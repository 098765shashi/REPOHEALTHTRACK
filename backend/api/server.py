import os, shutil, traceback
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db.database import init_db, get_db
from db.models import Repository, User
from db.schemas import AnalyzeRequest, RepoOut, MetricsOut, UserCreate, UserLogin, Token
from api.auth import hash_pw, verify_pw, make_token, current_user

from ingest.git_walker import clone_repo, walk_commits
from analyze.complexity import repo_complexity
from analyze.ownership import ownership, author_ownership
from analyze.bus_factor import bus_factor
from analyze.hotspots import hotspots
from analyze.coupling import co_change
from analyze.architecture import detect_cycles
from graph.graph_builder import build_import_graph, graph_to_json
from score.health_scorer import compute_health
from score.trend_analyzer import commit_timeline
from score.llm_narrator import generate_report

app = FastAPI(title="Repo Health Intelligence", version="1.0.0")
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/")
def root():
    return {"name": "Repo Health Intelligence", "status": "ok"}

# ---------- Auth ----------
@app.post("/auth/signup", response_model=Token)
def signup(body: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(400, "Email already registered")
    u = User(email=body.email, password_hash=hash_pw(body.password))
    db.add(u); db.commit()
    return Token(access_token=make_token(u.email))

@app.post("/auth/login", response_model=Token)
def login(body: UserLogin, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == body.email).first()
    if not u or not verify_pw(body.password, u.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return Token(access_token=make_token(u.email))

# ---------- Analyze ----------
def _run_analysis(repo_id: int):
    from db.database import SessionLocal
    db = SessionLocal()
    repo = db.query(Repository).get(repo_id)
    tmp = None
    try:
        repo.status = "analyzing"; db.commit()
        tmp = clone_repo(repo.url, repo.branch)
        walked = walk_commits(tmp)
        cx = repo_complexity(tmp)
        hs = hotspots(cx, walked["file_churn"])
        own = ownership(walked["file_authors"])
        bf = bus_factor(walked["author_commits"])
        auth_share = author_ownership(walked["file_authors"])
        g = build_import_graph(tmp)
        cycles = detect_cycles(g)
        graph_json = graph_to_json(g)
        commits_files = []
        # build co-change from per-commit file lists (re-walk briefly)
        from git import Repo
        r = Repo(tmp)
        for i, c in enumerate(r.iter_commits()):
            if i >= 300: break
            commits_files.append(list(c.stats.files.keys()))
        coupling = co_change(commits_files)
        timeline = commit_timeline(walked["commits"])

        metrics = {
            "complexity": cx,
            "hotspots": hs,
            "ownership": own,
            "author_ownership": auth_share,
            "bus_factor": bf,
            "cycles": cycles,
            "graph": graph_json,
            "coupling": coupling,
            "timeline": timeline,
            "commits": walked["commits"][:100],
            "totals": {
                "files": len(cx),
                "commits": len(walked["commits"]),
                "authors": len(walked["author_commits"]),
            },
        }
        health = compute_health(metrics)
        metrics["health"] = health
        repo.metrics = metrics
        repo.health_score = health["score"]
        repo.ai_report = generate_report(repo.name, metrics, health)
        repo.status = "done"
        repo.error = None
    except Exception as e:
        repo.status = "error"
        repo.error = f"{e}\n{traceback.format_exc()[:1000]}"
    finally:
        if tmp: shutil.rmtree(tmp, ignore_errors=True)
        db.commit(); db.close()

@app.post("/analyze", response_model=RepoOut)
def analyze(body: AnalyzeRequest, bg: BackgroundTasks, db: Session = Depends(get_db),
            user=Depends(current_user)):
    name = body.url.rstrip("/").split("/")[-1].replace(".git", "")
    repo = Repository(url=body.url, name=name, branch=body.branch, status="pending",
                      user_id=user.id if user else None)
    db.add(repo); db.commit(); db.refresh(repo)
    bg.add_task(_run_analysis, repo.id)
    return repo

@app.get("/repositories", response_model=list[RepoOut])
def list_repos(db: Session = Depends(get_db)):
    return db.query(Repository).order_by(Repository.created_at.desc()).all()

def _get_repo(repo_id: int, db: Session) -> Repository:
    r = db.query(Repository).get(repo_id)
    if not r: raise HTTPException(404, "Repository not found")
    return r

@app.get("/metrics/{repo_id}", response_model=MetricsOut)
def get_metrics(repo_id: int, db: Session = Depends(get_db)):
    r = _get_repo(repo_id, db)
    return MetricsOut(repo_id=r.id, metrics=r.metrics or {}, ai_report=r.ai_report)

@app.get("/health/{repo_id}")
def get_health(repo_id: int, db: Session = Depends(get_db)):
    r = _get_repo(repo_id, db)
    return (r.metrics or {}).get("health", {"score": r.health_score})

@app.get("/hotspots/{repo_id}")
def get_hotspots(repo_id: int, db: Session = Depends(get_db)):
    r = _get_repo(repo_id, db)
    return (r.metrics or {}).get("hotspots", [])

@app.get("/contributors/{repo_id}")
def get_contributors(repo_id: int, db: Session = Depends(get_db)):
    r = _get_repo(repo_id, db)
    m = r.metrics or {}
    return {"bus_factor": m.get("bus_factor", {}), "authors": m.get("author_ownership", [])}

@app.get("/graph/{repo_id}")
def get_graph(repo_id: int, db: Session = Depends(get_db)):
    r = _get_repo(repo_id, db)
    return (r.metrics or {}).get("graph", {"nodes": [], "edges": []})

@app.get("/repository/{repo_id}", response_model=RepoOut)
def get_repo(repo_id: int, db: Session = Depends(get_db)):
    return _get_repo(repo_id, db)
