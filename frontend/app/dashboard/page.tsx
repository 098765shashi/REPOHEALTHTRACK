"use client";
import { useState } from "react";
import Link from "next/link";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import Nav from "@/components/Nav";
import { motion } from "framer-motion";
import { Loader2, Plus, ExternalLink } from "lucide-react";

export default function Dashboard() {
  const [url, setUrl] = useState("");
  const [branch, setBranch] = useState("main");
  const qc = useQueryClient();
  const { data: repos = [], isLoading } = useQuery({
    queryKey: ["repos"], queryFn: api.list, refetchInterval: 4000,
  });
  const mut = useMutation({
    mutationFn: () => api.analyze(url, branch),
    onSuccess: () => { setUrl(""); qc.invalidateQueries({ queryKey: ["repos"] }); },
  });

  return (
    <>
      <Nav />
      <main className="max-w-7xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-white/60 mt-1">Analyze any public GitHub repository.</p>

        <div className="card mt-6">
          <form onSubmit={e => { e.preventDefault(); if (url) mut.mutate(); }}
                className="flex flex-col md:flex-row gap-3">
            <input className="input flex-1" placeholder="https://github.com/owner/repo"
                   value={url} onChange={e => setUrl(e.target.value)} />
            <input className="input md:w-40" placeholder="branch" value={branch}
                   onChange={e => setBranch(e.target.value)} />
            <button className="btn-primary" disabled={mut.isPending}>
              {mut.isPending ? <Loader2 className="animate-spin" size={16}/> : <Plus size={16}/>}
              Analyze
            </button>
          </form>
          {mut.isError && <div className="text-bad text-sm mt-3">{(mut.error as Error).message}</div>}
        </div>

        <div className="mt-8 grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {isLoading && <div className="text-white/60">Loading…</div>}
          {repos.map((r: any) => (
            <motion.div key={r.id} layout className="card hover:border-accent/60 transition">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="font-semibold">{r.name}</div>
                  <div className="text-xs text-white/50 truncate max-w-[220px]">{r.url}</div>
                </div>
                <a href={r.url} target="_blank" rel="noreferrer" className="text-white/50 hover:text-white">
                  <ExternalLink size={16}/>
                </a>
              </div>
              <div className="mt-4 flex items-center gap-4">
                <div className="text-3xl font-bold">{Math.round(r.health_score)}</div>
                <div className="text-xs text-white/60">
                  <div>branch: {r.branch}</div>
                  <div>status: <span className={
                    r.status === "done" ? "text-good" :
                    r.status === "error" ? "text-bad" : "text-warn"
                  }>{r.status}</span></div>
                </div>
              </div>
              <Link href={`/repo/${r.id}`} className="btn-ghost w-full justify-center mt-4">Open details</Link>
            </motion.div>
          ))}
          {!isLoading && repos.length === 0 && (
            <div className="text-white/50">No repositories yet. Paste a GitHub URL above.</div>
          )}
        </div>
      </main>
    </>
  );
}
