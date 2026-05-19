"use client";
import { useState } from "react";
import Nav from "@/components/Nav";
import { API_URL } from "@/lib/api";

export default function Login() {
  const [mode, setMode] = useState<"login"|"signup">("login");
  const [email, setEmail] = useState(""); const [pw, setPw] = useState("");
  const [msg, setMsg] = useState("");
  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setMsg("");
    const res = await fetch(`${API_URL}/auth/${mode}`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password: pw }),
    });
    if (!res.ok) { setMsg(await res.text()); return; }
    const data = await res.json();
    localStorage.setItem("token", data.access_token);
    window.location.href = "/dashboard";
  }
  return (
    <>
      <Nav />
      <main className="max-w-md mx-auto px-6 py-20">
        <div className="card">
          <h1 className="text-2xl font-bold">{mode === "login" ? "Sign in" : "Create account"}</h1>
          <form onSubmit={submit} className="mt-6 space-y-3">
            <input className="input" placeholder="email" type="email" value={email} onChange={e=>setEmail(e.target.value)} required />
            <input className="input" placeholder="password" type="password" value={pw} onChange={e=>setPw(e.target.value)} required />
            <button className="btn-primary w-full justify-center">{mode === "login" ? "Sign in" : "Sign up"}</button>
          </form>
          {msg && <div className="text-bad text-sm mt-3">{msg}</div>}
          <button onClick={() => setMode(mode === "login" ? "signup" : "login")} className="mt-4 text-sm text-white/60 hover:text-white">
            {mode === "login" ? "Need an account? Sign up" : "Have an account? Sign in"}
          </button>
        </div>
      </main>
    </>
  );
}
