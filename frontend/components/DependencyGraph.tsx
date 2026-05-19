"use client";
import { useEffect, useRef } from "react";

export default function DependencyGraph({ data }: { data: { nodes: any[]; edges: any[] } }) {
  const ref = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    if (!ref.current || !data?.nodes?.length) return;
    const canvas = ref.current;
    const ctx = canvas.getContext("2d")!;
    const W = canvas.width = canvas.offsetWidth * devicePixelRatio;
    const H = canvas.height = canvas.offsetHeight * devicePixelRatio;
    ctx.scale(1, 1);
    const N = data.nodes.slice(0, 80);
    const idx = new Map(N.map((n, i) => [n.id, i]));
    const pos = N.map((_, i) => {
      const a = (i / N.length) * Math.PI * 2;
      const r = Math.min(W, H) * 0.38;
      return { x: W/2 + Math.cos(a)*r, y: H/2 + Math.sin(a)*r };
    });
    ctx.strokeStyle = "rgba(124,92,255,.25)";
    ctx.lineWidth = 1;
    data.edges.forEach(e => {
      const a = idx.get(e.source), b = idx.get(e.target);
      if (a == null || b == null) return;
      ctx.beginPath(); ctx.moveTo(pos[a].x, pos[a].y); ctx.lineTo(pos[b].x, pos[b].y); ctx.stroke();
    });
    pos.forEach(p => {
      ctx.beginPath(); ctx.fillStyle = "#22d3ee";
      ctx.arc(p.x, p.y, 4*devicePixelRatio, 0, Math.PI*2); ctx.fill();
    });
  }, [data]);
  return <canvas ref={ref} className="w-full h-[420px] rounded-xl bg-black/30" />;
}
