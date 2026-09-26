import { useState } from "react";
import { Activity, Settings2 } from "lucide-react";
import { runSimulation } from "../services/api";
import type { SimulationConfig, SimulationResult } from "../types/simulation";
import { SimulationForm } from "../components/simulation/SimulationForm";
import { ResultsPanel } from "../components/simulation/ResultsPanel";

const initialConfig: SimulationConfig = {
  agents: { numAgents: 100, greedyPercentage: 50, cooperativePercentage: 30, riskAversePercentage: 20 },
  environment: { initialResources: 1000, regenerationRate: 2, rounds: 500 },
  governance: { quotaEnabled: true, quotaLimit: 20, taxEnabled: false, taxRate: 0 },
};

export function Simulation() {
  const [config, setConfig] = useState(initialConfig);
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [running, setRunning] = useState(false);
  const execute = async () => { setRunning(true); setResult(null); try { setResult(await runSimulation(config)); } finally { setRunning(false); } };
  return (
    <div className="mx-auto max-w-[1440px] px-5 pb-16 pt-8 sm:px-8 sm:pt-12">
      <div className="mb-9 flex flex-col justify-between gap-5 border-b border-ink/10 pb-8 lg:flex-row lg:items-end"><div><p className="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em] text-teal"><Activity size={14} /> Simulation mode</p><h1 className="font-display text-4xl font-bold tracking-[-0.035em] sm:text-5xl">Experimental dashboard</h1><p className="mt-3 max-w-2xl text-base leading-7 text-ink/55">Shape the conditions of a commons experiment, then inspect the resource and wealth trajectories.</p></div><div className="flex items-center gap-2 text-xs text-ink/45"><Settings2 size={15} /> Mock API connected</div></div>
      <div className="grid items-start gap-6 xl:grid-cols-[390px_1fr]"><SimulationForm config={config} running={running} onChange={setConfig} onRun={execute} /><ResultsPanel result={result} /></div>
    </div>
  );
}
