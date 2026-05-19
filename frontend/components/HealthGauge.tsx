"use client";
import { motion } from "framer-motion";
export default function HealthGauge({ score = 0 }: { score: number }) {
  const color = score >= 85 ? "#22c55e" : score >= 70 ? "#84cc16" : score >= 50 ? "#f59e0b" : "#ef4444";
  const r = 70, c = 2 * Math.PI * r;
  const off = c - (score / 100) * c;
  return (
    <div className="relative w-44 h-44">
      <svg viewBox="0 0 160 160" className="w-full h-full -rotate-90">
        <circle cx="80" cy="80" r={r} stroke="#1f2230" strokeWidth="14" fill="none" />
        <motion.circle cx="80" cy="80" r={r} stroke={color} strokeWidth="14" strokeLinecap="round" fill="none"
          strokeDasharray={c} initial={{ strokeDashoffset: c }} animate={{ strokeDashoffset: off }}
          transition={{ duration: 1.2, ease: "easeOut" }} />
      </svg>
      <div className="absolute inset-0 grid place-items-center text-center">
        <div>
          <div className="text-4xl font-bold">{Math.round(score)}</div>
          <div className="text-xs text-white/60">Health score</div>
        </div>
      </div>
    </div>
  );
}
