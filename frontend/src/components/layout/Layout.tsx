import { Link, NavLink } from "react-router-dom";
import { FlaskConical, LayoutDashboard } from "lucide-react";
import type { ReactNode } from "react";

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-paper text-ink">
      <header className="border-b border-ink/10 bg-paper/95 backdrop-blur">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between px-5 py-4 sm:px-8">
          <Link to="/" className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-ink text-paper">
              <FlaskConical size={18} strokeWidth={2.2} />
            </span>
            <span>
              <span className="block font-display text-sm font-bold tracking-tight">CommonsSim</span>
              <span className="block text-[11px] uppercase tracking-[0.18em] text-ink/50">Research platform</span>
            </span>
          </Link>
          <nav className="flex items-center gap-1 rounded-full border border-ink/10 bg-white/60 p-1 text-sm">
            <NavLink to="/" className={({ isActive }) => `rounded-full px-4 py-2 transition ${isActive ? "bg-ink text-paper" : "text-ink/60 hover:text-ink"}`}>
              Overview
            </NavLink>
            <NavLink to="/simulation" className={({ isActive }) => `flex items-center gap-2 rounded-full px-4 py-2 transition ${isActive ? "bg-ink text-paper" : "text-ink/60 hover:text-ink"}`}>
              <LayoutDashboard size={15} /> Simulation
            </NavLink>
          </nav>
        </div>
      </header>
      <main>{children}</main>
    </div>
  );
}
