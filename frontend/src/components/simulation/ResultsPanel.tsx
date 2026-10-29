import { Activity, CheckCircle2, LineChart as LineChartIcon } from "lucide-react";
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { SimulationResult } from "../../types/simulation";
import { ChartCard } from "../ui/ChartCard";
import { MetricCard } from "../ui/MetricCard";

export function ResultsPanel({ result }: { result: SimulationResult | null }) {
  if (!result) {
    return <div className="flex min-h-[520px] flex-col items-center justify-center rounded-2xl border border-dashed border-ink/15 bg-white/45 p-8 text-center"><span className="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-teal/10 text-teal"><LineChartIcon size={25} /></span><h2 className="font-display text-xl font-bold">Your results will appear here</h2><p className="mt-2 max-w-sm text-sm leading-6 text-ink/50">Configure the experimental conditions, then run a simulation to inspect resource sustainability and agent wealth.</p></div>;
  }
  return (
    <div className="space-y-5">
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard metric={{ label: "Remaining resource", value: result.remainingResource.toLocaleString(), detail: "units at final round", tone: "teal" }} />
        <MetricCard metric={{ label: "Average wealth", value: result.averageWealth.toFixed(1), detail: "per agent", tone: "ink" }} />
        <MetricCard metric={{ label: "Average trust", value: `${(result.averageTrust * 100).toFixed(0)}%`, detail: "population signal", tone: "neutral" }} />
        <MetricCard metric={{ label: "Simulation status", value: result.status, detail: "resource trajectory", tone: result.status === "Resource Sustained" ? "teal" : "coral" }} />
      </div>
      <div className="grid gap-5 xl:grid-cols-2">
        <ChartCard title="Resource vs time" detail="Available commons resource by round"><Chart data={result.chartData} dataKey="resourceLevel" color="#087f8c" label="Resource" /></ChartCard>
        <ChartCard title="Average wealth" detail="Mean accumulated wealth by round"><Chart data={result.chartData} dataKey="averageWealth" color="#e9795f" label="Wealth" /></ChartCard>
      </div>
      <div className="flex items-center gap-3 rounded-2xl border border-teal/15 bg-teal/[0.06] px-5 py-4 text-sm text-ink/70"><CheckCircle2 size={18} className="text-teal" /><span>Simulation complete at {new Date(result.completedAt).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}.</span></div>
    </div>
  );
}

function Chart({ data, dataKey, color, label }: { data: SimulationResult["chartData"]; dataKey: "resourceLevel" | "averageWealth"; color: string; label: string }) {
  return <div className="h-64 w-full"><ResponsiveContainer width="100%" height="100%"><LineChart data={data} margin={{ top: 8, right: 8, left: -18, bottom: 0 }}><CartesianGrid stroke="#17252a" strokeOpacity={0.08} vertical={false} /><XAxis dataKey="round" tickLine={false} axisLine={false} tick={{ fontSize: 11, fill: "#17252a", opacity: 0.45 }} /><YAxis tickLine={false} axisLine={false} tick={{ fontSize: 11, fill: "#17252a", opacity: 0.45 }} /><Tooltip contentStyle={{ borderRadius: 12, border: "1px solid rgba(23,37,42,.1)", boxShadow: "0 8px 20px rgba(23,37,42,.1)" }} formatter={(value) => [typeof value === "number" ? value.toFixed(1) : "—", label]} /><Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2.5} dot={false} activeDot={{ r: 4, strokeWidth: 0 }} /></LineChart></ResponsiveContainer></div>;
}
