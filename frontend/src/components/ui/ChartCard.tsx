import type { ReactNode } from "react";

export function ChartCard({ title, detail, children }: { title: string; detail: string; children: ReactNode }) {
  return (
    <section className="rounded-2xl border border-ink/10 bg-white p-5 shadow-[0_12px_35px_rgba(23,37,42,0.05)] sm:p-6">
      <div className="mb-5 flex items-end justify-between gap-4">
        <div>
          <h3 className="font-display text-lg font-bold tracking-tight">{title}</h3>
          <p className="mt-1 text-sm text-ink/50">{detail}</p>
        </div>
        <span className="hidden h-2 w-2 rounded-full bg-teal sm:block" />
      </div>
      {children}
    </section>
  );
}
