"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import { Activity, GitBranch, Sparkles, Network, Users, Flame } from "lucide-react";
import Nav from "@/components/Nav";

const Feature = ({ icon: Icon, title, desc }: any) => (
  <motion.div whileHover={{ y: -4 }} className="card">
    <Icon className="text-accent" />
    <div className="mt-3 font-semibold">{title}</div>
    <div className="text-sm text-white/60 mt-1">{desc}</div>
  </motion.div>
);

export default function Home() {
  return (
    <>
      <Nav />
      <section className="relative bg-grad-hero">
        <div className="max-w-7xl mx-auto px-6 pt-24 pb-32 text-center">
          <motion.div initial={{opacity:0,y:10}} animate={{opacity:1,y:0}}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-border text-xs text-white/70">
            <Sparkles size={14} className="text-accent2"/> AI-powered engineering analytics
          </motion.div>
          <motion.h1 initial={{opacity:0,y:20}} animate={{opacity:1,y:0}} transition={{delay:.1}}
            className="mt-6 text-5xl md:text-7xl font-bold tracking-tight">
            See your repo's <span className="bg-gradient-to-r from-accent to-accent2 bg-clip-text text-transparent">true health</span>
          </motion.h1>
          <p className="mt-6 max-w-2xl mx-auto text-white/70 text-lg">
            Detect hotspots, bus-factor risk, architectural decay, and complexity drift —
            with an AI executive summary for every repository.
          </p>
          <div className="mt-8 flex justify-center gap-3">
            <Link href="/dashboard" className="btn-primary">Analyze a repository</Link>
            <a href="#features" className="btn-ghost">See features</a>
          </div>
        </div>
      </section>

      <section id="features" className="max-w-7xl mx-auto px-6 pb-24 grid md:grid-cols-3 gap-5">
        <Feature icon={Activity} title="Health Score" desc="Weighted 0–100 score across complexity, hotspots, bus factor, and dependencies." />
        <Feature icon={Flame} title="Hotspot Detection" desc="Files that are both complex and frequently changed — the real refactor targets." />
        <Feature icon={Users} title="Bus Factor" desc="Concentration risk across contributors with ownership share per file." />
        <Feature icon={Network} title="Dependency Graph" desc="Module import graph with cycle detection and coupling analysis." />
        <Feature icon={GitBranch} title="Commit Intelligence" desc="Churn, ownership, co-change clusters across recent history." />
        <Feature icon={Sparkles} title="AI Narrative" desc="Executive summary, risk insights, and recommendations from GPT." />
      </section>

      <footer className="border-t border-border py-8 text-center text-sm text-white/40">
        Built for engineering teams who care. © Repo Health Intelligence
      </footer>
    </>
  );
}
