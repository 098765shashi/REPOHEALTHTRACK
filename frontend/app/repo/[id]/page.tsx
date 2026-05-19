"use client";
import { use } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import Nav from "@/components/Nav";
import HealthGauge from "@/components/HealthGauge";
import DependencyGraph from "@/components/DependencyGraph";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from "recharts";
import { motion } from "framer-motion";
import { Flame, Users, GitCommit, Network, Sparkles, AlertTriangle } from "lucide-react";

const COLORS = ["#7c5cff","#22d3ee","#22c55e","#f59e0b","#ef4444","#a78bfa","#34d399"];

export default function RepoPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const repoId = parseInt(id);
  const { data: repo } = useQuery({ queryKey: ["repo", repoId], queryFn: () => api.repo(repoId), refetchInterval: 3000 });
  const { data: m } = useQuery({
    queryKey: ["metrics", repoId], queryFn: () => api.metrics(repoId),
    enabled: repo?.status === "done", refetchInterval: false,
  });

  if (!repo) return <><Nav /><div className="p-10 text-white/60">Loading…</div></>;
  if (repo.status !== "done") return (
    <><Nav />
      <main className="max-w-3xl mx-auto px-6 py-20 text-center">
        <h1 className="text-2xl font-semibold">{repo.name}</h1>
        <p className="mt-2 text-white/60">Status: <span className="text-warn">{repo.status}</span></p>
        <p className="text-sm text-white/50 mt-1">{repo.error || "Analyzing — this can take 30–90s depending on repo size."}</p>
        <div className="mt-8 h-1.5 w-full bg-border rounded-full overflow-hidden">
          <motion.div className="h-full bg-accent" initial={{width:"5%"}} animate={{width:"90%"}} transition={{duration:30}} />
        </div>
      </main>
    </>
  );

  const metrics = m?.metrics || {};
  const health = metrics.health || { score: repo.health_score, breakdown: {} };
  const hotspots = (metrics.hotspots || []).slice(0, 10);
  const timeline = metrics.timeline || [];
  const authors = (metrics.author_ownership || []).slice(0, 7);
  const bf = metrics.bus_factor || {};
  const cycles = metrics.cycles || [];
  const totals = metrics.totals || {};

  return (
    <>
      <Nav />
      <main className="max-w-7xl mx-auto px-6 py-10 space-y-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold">{repo.name}</h1>
            <a href={repo.url} target="_blank" rel="noreferrer" className="text-sm text-white/50 hover:text-white">{repo.url}</a>
          </div>
          <div className="flex gap-3 text-sm text-white/70">
            <span className="card !p-3">Files: <b>{totals.files ?? 0}</b></span>
            <span className="card !p-3">Commits: <b>{totals.commits ?? 0}</b></span>
            <span className="card !p-3">Authors: <b>{totals.authors ?? 0}</b></span>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-5">
          <div className="card flex items-center gap-6">
            <HealthGauge score={health.score} />
            <div className="space-y-1 text-sm">
              <div className="text-white/60">Risk breakdown</div>
              {Object.entries(health.breakdown || {}).map(([k,v]: any) => (
                <div key={k} className="flex items-center gap-2">
                  <div className="w-28 capitalize text-white/70">{k.replace("_"," ")}</div>
                  <div className="flex-1 h-2 bg-border rounded-full overflow-hidden">
                    <div className="h-full bg-accent" style={{ width: `${(v*100).toFixed(0)}%` }}/>
                  </div>
                  <div className="w-10 text-right">{(v*100).toFixed(0)}%</div>
                </div>
              ))}
            </div>
          </div>

          <div className="card lg:col-span-2">
            <div className="flex items-center gap-2 mb-3"><Sparkles className="text-accent2" size={18}/><b>AI insights</b></div>
            <div className="text-sm whitespace-pre-wrap text-white/80 leading-relaxed">{m?.ai_report || "Generating…"}</div>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-5">
          <div className="card">
            <div className="flex items-center gap-2 mb-3"><GitCommit size={18} className="text-accent"/><b>Commit activity</b></div>
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={timeline}>
                <XAxis dataKey="date" stroke="#666" tick={{fontSize:10}} />
                <YAxis stroke="#666" tick={{fontSize:10}} />
                <Tooltip contentStyle={{background:"#0f1117",border:"1px solid #1f2230"}}/>
                <Line type="monotone" dataKey="commits" stroke="#7c5cff" strokeWidth={2} dot={false}/>
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="card">
            <div className="flex items-center gap-2 mb-3"><Flame size={18} className="text-bad"/><b>Top hotspots</b></div>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={hotspots} layout="vertical" margin={{left: 80}}>
                <XAxis type="number" stroke="#666" tick={{fontSize:10}}/>
                <YAxis dataKey="file" type="category" stroke="#666" tick={{fontSize:10}} width={140}
                       tickFormatter={(v:string) => v.split("/").slice(-1)[0]}/>
                <Tooltip contentStyle={{background:"#0f1117",border:"1px solid #1f2230"}}/>
                <Bar dataKey="score" fill="#ef4444"/>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="card">
            <div className="flex items-center gap-2 mb-3"><Users size={18} className="text-accent2"/><b>Contributor ownership</b></div>
            <div className="flex items-center gap-4">
              <ResponsiveContainer width="50%" height={220}>
                <PieChart>
                  <Pie data={authors} dataKey="share" nameKey="author" outerRadius={80}>
                    {authors.map((_:any,i:number) => <Cell key={i} fill={COLORS[i%COLORS.length]}/>)}
                  </Pie>
                  <Tooltip contentStyle={{background:"#0f1117",border:"1px solid #1f2230"}}/>
                </PieChart>
              </ResponsiveContainer>
              <div className="flex-1 text-sm space-y-1">
                <div className="text-white/60 mb-2">Bus factor: <b className="text-white">{bf.bus_factor ?? "?"}</b> {bf.risk > 0.5 && <span className="text-warn ml-2">⚠ concentration</span>}</div>
                {authors.map((a:any,i:number) => (
                  <div key={a.author} className="flex justify-between">
                    <span><span className="inline-block w-2 h-2 rounded-full mr-2" style={{background:COLORS[i%COLORS.length]}}/>{a.author}</span>
                    <span className="text-white/60">{(a.share*100).toFixed(1)}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center gap-2 mb-3"><Network size={18} className="text-accent"/><b>Dependency graph</b></div>
            <DependencyGraph data={metrics.graph || {nodes:[],edges:[]}} />
          </div>
        </div>

        {cycles.length > 0 && (
          <div className="card border-warn/40">
            <div className="flex items-center gap-2 mb-3"><AlertTriangle className="text-warn" size={18}/><b>Circular dependencies ({cycles.length})</b></div>
            <ul className="text-sm space-y-1 text-white/70 max-h-48 overflow-auto">
              {cycles.slice(0,10).map((c:any,i:number) => (
                <li key={i} className="font-mono text-xs">{c.join(" → ")} → {c[0]}</li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </>
  );
}
