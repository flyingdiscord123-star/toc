import axios from "axios";
import type { SimulationConfig, SimulationResult } from "../types/simulation";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export async function runSimulation(config: SimulationConfig): Promise<SimulationResult> {
  const { data } = await api.post<SimulationResult>("/api/simulations", config);
  return data;
}
