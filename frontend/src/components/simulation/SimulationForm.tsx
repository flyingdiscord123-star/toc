import { Play, RotateCcw } from "lucide-react";
import type { SimulationConfig } from "../../types/simulation";
import { SectionCard } from "../ui/SectionCard";

type Props = {
  config: SimulationConfig;
  running: boolean;
  onChange: (config: SimulationConfig) => void;
  onRun: () => void;
};

function rebalancePercentages(config: SimulationConfig, key: "greedyPercentage" | "cooperativePercentage" | "riskAversePercentage", value: number): SimulationConfig {
  const next = { ...config, agents: { ...config.agents, [key]: value } };
  const otherKeys = (["greedyPercentage", "cooperativePercentage", "riskAversePercentage"] as const).filter((item) => item !== key);
  const remaining = 100 - value;
  const currentOtherTotal = otherKeys.reduce((sum, item) => sum + config.agents[item], 0);
  const first = currentOtherTotal === 0 ? remaining / 2 : Math.round((config.agents[otherKeys[0]] / currentOtherTotal) * remaining);
  const second = remaining - first;
  next.agents[otherKeys[0]] = Math.max(0, first);
  next.agents[otherKeys[1]] = Math.max(0, second);
  return next;
}

function Slider({ label, value, min, max, step = 1, suffix = "", onChange }: { label: string; value: number; min: number; max: number; step?: number; suffix?: string; onChange: (value: number) => void }) {
  return (
    <label className="block">
      <span className="mb-2 flex items-center justify-between text-sm font-semibold">
        <span>{label}</span>
        <span className="font-display text-sm text-teal">{value}{suffix}</span>
      </span>
      <input className="range-input" type="range" min={min} max={max} step={step} value={value} onChange={(event) => onChange(Number(event.target.value))} />
      <span className="mt-1 flex justify-between text-[11px] text-ink/35"><span>{min}{suffix}</span><span>{max}{suffix}</span></span>
    </label>
  );
}

export function SimulationForm({ config, running, onChange, onRun }: Props) {
  const reset = () => onChange({
    agents: { numAgents: 100, greedyPercentage: 50, cooperativePercentage: 30, riskAversePercentage: 20 },
    environment: { initialResources: 1000, regenerationRate: 2, rounds: 500 },
    governance: { quotaEnabled: true, quotaLimit: 20, taxEnabled: false, taxRate: 0 },
  });
  return (
    <div className="space-y-5">
      <SectionCard eyebrow="01 / Population" title="Heterogeneous agents" description="Tune the composition of the commons population.">
        <div className="space-y-6">
          <Slider label="Number of agents" value={config.agents.numAgents} min={10} max={500} step={10} onChange={(value) => onChange({ ...config, agents: { ...config.agents, numAgents: value } })} />
          <div className="rounded-xl bg-fog/55 p-4">
            <div className="mb-4 flex items-center justify-between"><span className="text-xs font-semibold uppercase tracking-[0.14em] text-ink/50">Population share</span><span className="rounded-full bg-teal/10 px-2 py-1 text-xs font-bold text-teal">{config.agents.greedyPercentage + config.agents.cooperativePercentage + config.agents.riskAversePercentage}% total</span></div>
            <div className="space-y-5">
              <Slider label="Greedy" value={config.agents.greedyPercentage} min={0} max={100} suffix="%" onChange={(value) => onChange(rebalancePercentages(config, "greedyPercentage", value))} />
              <Slider label="Cooperative" value={config.agents.cooperativePercentage} min={0} max={100} suffix="%" onChange={(value) => onChange(rebalancePercentages(config, "cooperativePercentage", value))} />
              <Slider label="Risk-averse" value={config.agents.riskAversePercentage} min={0} max={100} suffix="%" onChange={(value) => onChange(rebalancePercentages(config, "riskAversePercentage", value))} />
            </div>
          </div>
        </div>
      </SectionCard>
      <SectionCard eyebrow="02 / Environment" title="Shared resource" description="Define the renewable commons and experimental horizon.">
        <div className="space-y-6">
          <Slider label="Initial resource" value={config.environment.initialResources} min={100} max={5000} step={50} onChange={(value) => onChange({ ...config, environment: { ...config.environment, initialResources: value } })} />
          <Slider label="Regeneration rate" value={config.environment.regenerationRate} min={0} max={10} step={0.5} suffix="%" onChange={(value) => onChange({ ...config, environment: { ...config.environment, regenerationRate: value } })} />
          <Slider label="Simulation rounds" value={config.environment.rounds} min={50} max={1000} step={50} onChange={(value) => onChange({ ...config, environment: { ...config.environment, rounds: value } })} />
        </div>
      </SectionCard>
      <SectionCard eyebrow="03 / Governance" title="Institutional controls" description="Governance is exogenous and fixed before a run begins.">
        <div className="space-y-6">
          <Slider label="Quota limit" value={config.governance.quotaLimit} min={0} max={50} step={1} onChange={(value) => onChange({ ...config, governance: { ...config.governance, quotaLimit: value } })} />
          <Slider label="Tax rate" value={config.governance.taxRate} min={0} max={30} step={1} suffix="%" onChange={(value) => onChange({ ...config, governance: { ...config.governance, taxRate: value } })} />
        </div>
      </SectionCard>
      <div className="flex items-center gap-3">
        <button className="button-primary flex-1" type="button" onClick={onRun} disabled={running}><Play size={17} fill="currentColor" />{running ? "Running experiment…" : "Run simulation"}</button>
        <button className="button-secondary" type="button" onClick={reset} aria-label="Reset configuration" title="Reset configuration"><RotateCcw size={17} /></button>
      </div>
    </div>
  );
}
