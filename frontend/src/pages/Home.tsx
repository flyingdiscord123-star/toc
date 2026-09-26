import { ArrowRight, BarChart3, SlidersHorizontal, Waves } from "lucide-react";
import { Link } from "react-router-dom";
import type { ReactNode } from "react";

export function Home() {
  return (
    <div className="mx-auto max-w-[1440px] px-5 pb-16 pt-10 sm:px-8 sm:pt-16">
      <div className="grid items-end gap-12 lg:grid-cols-[1.1fr_.9fr] lg:gap-20">
        <div>
          <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-teal/20 bg-teal/5 px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.16em] text-teal"><span className="h-1.5 w-1.5 rounded-full bg-teal" /> Research workspace</p>
          <h1 className="max-w-3xl font-display text-5xl font-bold leading-[1.04] tracking-[-0.04em] sm:text-7xl">Study the commons <span className="text-teal">in motion.</span></h1>
          <p className="mt-7 max-w-xl text-lg leading-8 text-ink/60">A focused environment for exploring how heterogeneous agents, renewable resources, and exogenous governance interact over time.</p>
          <Link to="/simulation" className="button-primary mt-9 inline-flex">Launch simulation <ArrowRight size={17} /></Link>
        </div>
        <div className="relative overflow-hidden rounded-3xl bg-ink p-7 text-paper shadow-[0_20px_45px_rgba(23,37,42,0.16)] sm:p-9"><div className="absolute -right-16 -top-16 h-44 w-44 rounded-full border-[22px] border-teal/25" /><div className="absolute -bottom-24 -left-12 h-44 w-44 rounded-full border-[22px] border-coral/20" /><div className="relative"><p className="text-xs font-semibold uppercase tracking-[0.16em] text-paper/45">Model outline</p><div className="mt-8 space-y-6"><FlowItem icon={<SlidersHorizontal size={17} />} title="Configure" text="Set population, environment, and quota conditions." /><FlowItem icon={<Waves size={17} />} title="Simulate" text="Observe a renewable resource shared by competing agents." /><FlowItem icon={<BarChart3 size={17} />} title="Compare" text="Read trajectories for resource sustainability and wealth." /></div></div></div>
      </div>
      <div className="mt-20 grid gap-4 border-t border-ink/10 pt-8 text-sm text-ink/55 sm:grid-cols-3"><p><strong className="font-display text-ink">3</strong><br />fixed agent archetypes</p><p><strong className="font-display text-ink">1</strong><br />shared renewable commons</p><p><strong className="font-display text-ink">0</strong><br />learning controls exposed</p></div>
    </div>
  );
}

function FlowItem({ icon, title, text }: { icon: ReactNode; title: string; text: string }) { return <div className="flex gap-4"><span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-paper/10 text-teal">{icon}</span><div><p className="font-display font-semibold">{title}</p><p className="mt-1 text-sm leading-5 text-paper/55">{text}</p></div></div>; }
