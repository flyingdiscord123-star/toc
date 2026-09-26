import axios from "axios";
import type { SimulationConfig, SimulationResult } from "../types/simulation";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

function buildMockResult(config: SimulationConfig): SimulationResult {
  const chartData = Array.from({ length: config.environment.rounds }, (_, index) => {
    const round = index + 1;
    const depletion = Math.min(0.72, (round / config.environment.rounds) * 0.72);
    const resourceLevel = Math.max(
      0,
      Math.round(config.environment.initialResources * (1 - depletion) * 10) / 10,
    );
    const extractionBias =
      config.agents.greedyPercentage * 0.012 +
      config.agents.cooperativePercentage * 0.004 +
      config.agents.riskAversePercentage * 0.002;
    const averageWealth = Math.round((round * extractionBias) * 10) / 10;
    return { round, resourceLevel, averageWealth };
  });

  const last = chartData.at(-1) ?? {
    resourceLevel: config.environment.initialResources,
    averageWealth: 0,
    round: 0,
  };

  return {
    status: last.resourceLevel > config.environment.initialResources * 0.12
      ? "Resource Sustained"
      : "Resource Collapsed",
    remainingResource: last.resourceLevel,
    averageWealth: last.averageWealth,
    averageTrust: 0.72,
    chartData,
    completedAt: new Date().toISOString(),
  };
}

export async function runSimulation(config: SimulationConfig): Promise<SimulationResult> {
  // Replace this mock with the FastAPI request when the backend endpoint is ready.
  await new Promise((resolve) => window.setTimeout(resolve, 550));
  return buildMockResult(config);
}
