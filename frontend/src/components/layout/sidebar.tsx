"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Droplets,
  MapPin,
  ListOrdered,
  BarChart3,
  Network,
  Waves,
  BookOpen,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface NavItem {
  label: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
}

const PRIMARY_NAV: NavItem[] = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "Geospatial Map",
    href: "/map",
    icon: MapPin,
  },
  {
    label: "Well Inventory",
    href: "/wells",
    icon: Droplets,
  },
  {
    label: "Active Testing Queue",
    href: "/testing-queue",
    icon: ListOrdered,
    badge: "50 Budget",
  },
];

const RESEARCH_NAV: NavItem[] = [
  {
    label: "Model Analytics",
    href: "/analytics",
    icon: BarChart3,
  },
  {
    label: "Bayesian Network (BBN)",
    href: "/models",
    icon: Network,
  },
];

const META_NAV: NavItem[] = [
  {
    label: "About & Overview",
    href: "/about",
    icon: BookOpen,
  },
];

export function Sidebar() {
  const pathname = usePathname();

  const isActive = (href: string) =>
    pathname === href || (href !== "/dashboard" && pathname.startsWith(href));

  return (
    <aside className="fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-slate-800/60 bg-[#0B0F19] text-slate-300">
      {/* Brand Header */}
      <Link
        href="/"
        className="flex h-16 items-center gap-3 border-b border-slate-800/60 px-5 transition-colors hover:bg-slate-800/40 group"
        title="Return to HydroScope product homepage"
      >
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600/15 text-blue-400 border border-blue-500/20 shadow-xs group-hover:bg-blue-600/25 group-hover:border-blue-400/40 transition-colors">
          <Waves className="h-5 w-5 text-blue-400" />
        </div>
        <div className="flex flex-col">
          <div className="flex items-center gap-1.5">
            <span className="text-sm font-semibold tracking-tight text-white group-hover:text-blue-300 transition-colors">
              HydroScope
            </span>
          </div>
          <span className="text-[11px] text-slate-400 font-medium">
            Groundwater Surveillance
          </span>
        </div>
      </Link>

      {/* Navigation Sections */}
      <div className="flex-1 overflow-y-auto px-3.5 py-5 space-y-6">
        {/* Primary Surveillance Operations */}
        <div>
          <div className="mb-2 px-2.5 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
            Surveillance & Monitoring
          </div>
          <nav className="space-y-0.5">
            {PRIMARY_NAV.map((item) => {
              const active = isActive(item.href);
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "group flex items-center justify-between rounded-lg px-3 py-2 text-xs font-medium transition-all",
                    active
                      ? "bg-blue-600/15 text-blue-300 font-semibold border border-blue-500/30"
                      : "text-slate-400 hover:bg-slate-800/60 hover:text-white"
                  )}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon
                      className={cn(
                        "h-4 w-4 shrink-0 transition-colors",
                        active
                          ? "text-blue-400"
                          : "text-slate-500 group-hover:text-slate-200"
                      )}
                    />
                    <span>{item.label}</span>
                  </div>

                  {item.badge && (
                    <span className="rounded-full bg-blue-950/80 px-2 py-0.5 text-[10px] font-medium text-blue-300 border border-blue-800/60">
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Separated ML Models & Research Subpart */}
        <div>
          <div className="mb-2 px-2.5 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
            ML Models & Research
          </div>
          <nav className="space-y-0.5">
            {RESEARCH_NAV.map((item) => {
              const active = isActive(item.href);
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "group flex items-center justify-between rounded-lg px-3 py-2 text-xs font-medium transition-all",
                    active
                      ? "bg-indigo-600/15 text-indigo-300 font-semibold border border-indigo-500/30"
                      : "text-slate-400 hover:bg-slate-800/60 hover:text-white"
                  )}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon
                      className={cn(
                        "h-4 w-4 shrink-0 transition-colors",
                        active
                          ? "text-indigo-400"
                          : "text-slate-500 group-hover:text-slate-200"
                      )}
                    />
                    <span>{item.label}</span>
                  </div>
                </Link>
              );
            })}
          </nav>
        </div>

        {/* About / Docs */}
        <div>
          <div className="mb-2 px-2.5 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
            Documentation
          </div>
          <nav className="space-y-0.5">
            {META_NAV.map((item) => {
              const active = isActive(item.href);
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "group flex items-center gap-2.5 rounded-lg px-3 py-2 text-xs font-medium transition-all",
                    active
                      ? "bg-slate-700/50 text-slate-200 font-semibold border border-slate-600/40"
                      : "text-slate-400 hover:bg-slate-800/60 hover:text-white"
                  )}
                >
                  <Icon
                    className={cn(
                      "h-4 w-4 shrink-0 transition-colors",
                      active
                        ? "text-slate-300"
                        : "text-slate-500 group-hover:text-slate-200"
                    )}
                  />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Refined Minimal Footer */}
      <div className="border-t border-slate-800/60 p-3.5">
        <div className="flex items-center justify-between rounded-lg bg-slate-900/60 px-3 py-2 border border-slate-800/40">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-400" />
            <span className="text-[11px] font-medium text-slate-300">
              5 Indian States Monitored
            </span>
          </div>
          <span className="text-[10px] font-mono text-slate-400">36.9k Wells</span>
        </div>
      </div>
    </aside>
  );
}
