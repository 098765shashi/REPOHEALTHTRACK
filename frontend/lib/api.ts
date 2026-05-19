export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
  return res.json();
}

export const api = {
  analyze: (url: string, branch = "main") =>
    req<any>("/analyze", { method: "POST", body: JSON.stringify({ url, branch }) }),
  list: () => req<any[]>("/repositories"),
  repo: (id: number) => req<any>(`/repository/${id}`),
  metrics: (id: number) => req<any>(`/metrics/${id}`),
  health: (id: number) => req<any>(`/health/${id}`),
  hotspots: (id: number) => req<any[]>(`/hotspots/${id}`),
  contributors: (id: number) => req<any>(`/contributors/${id}`),
  graph: (id: number) => req<any>(`/graph/${id}`),
};
