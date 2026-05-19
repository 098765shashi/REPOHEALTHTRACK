"use client";
import Link from "next/link";
import { Activity } from "lucide-react";
export default function Nav() {
  return (
    <header className="sticky top-0 z-30 backdrop-blur-md border-b border-border bg-bg/70">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <Activity className="text-accent" size={22} />
          <span>Repo Health <span className="text-accent2">Intelligence</span></span>
        </Link>
        <nav className="flex items-center gap-6 text-sm text-white/70">
          <Link href="/dashboard" className="hover:text-white">Dashboard</Link>
          <Link href="/login" className="btn-ghost">Sign in</Link>
          <Link href="/dashboard" className="btn-primary">Analyze repo</Link>
        </nav>
      </div>
    </header>
  );
}
