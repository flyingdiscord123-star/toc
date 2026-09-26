import type { ReactNode } from "react";

export function SectionCard({ eyebrow, title, description, children }: { eyebrow: string; title: string; description?: string; children: ReactNode }) {
  return (
    <section className="rounded-2xl border border-ink/10 bg-white p-5 shadow-[0_12px_35px_rgba(23,37,42,0.05)] sm:p-6">
      <div className="mb-6 border-b border-ink/10 pb-4">
        <p className="mb-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-teal">{eyebrow}</p>
        <h2 className="font-display text-xl font-bold tracking-tight">{title}</h2>
        {description && <p className="mt-1 text-sm text-ink/55">{description}</p>}
      </div>
      {children}
    </section>
  );
}
