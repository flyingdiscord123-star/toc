import { ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";
import type { MetricCardData } from "../../types/simulation";

const toneMap = {
  teal: "border-teal/20 bg-teal/[0.06] text-teal",
  coral: "border-coral/25 bg-coral/[0.07] text-coral",
  ink: "border-ink/15 bg-ink/[0.04] text-ink",
  neutral: "border-ink/10 bg-white text-ink",
};

export function MetricCard({ metric }: { metric: MetricCardData }) {
  const Icon = metric.tone === "coral" ? ArrowDownRight : metric.tone === "teal" ? ArrowUpRight : Minus;
  return (
    <article className={`rounded-2xl border p-5 ${toneMap[metric.tone ?? "neutral"]}`}>
      <div className="mb-8 flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-ink/50">{metric.label}</p>
        <Icon size={16} className="opacity-60" />
      </div>
      <p className="font-display text-2xl font-bold tracking-tight">{metric.value}</p>
      {metric.detail && <p className="mt-1 text-sm text-ink/50">{metric.detail}</p>}
    </article>
  );
}
