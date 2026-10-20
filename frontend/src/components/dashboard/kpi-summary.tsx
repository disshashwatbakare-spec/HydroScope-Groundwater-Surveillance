"use client";

import * as React from "react";
import {
  Droplets,
  AlertTriangle,
  Activity,
  Sparkles,
  ArrowUpRight,
  ShieldAlert,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { formatNumber, formatPct } from "@/lib/utils";
import type { DashboardKPIs } from "@/types";

interface KpiSummaryProps {
  kpis: DashboardKPIs;
}

export function KpiSummary({ kpis }: KpiSummaryProps) {
  const cards = [
    {
      title: "Monitored Wells",
      value: formatNumber(kpis.totalWells),
      description: "Across 5 states (MH, AP, WB, RJ, GJ)",
      icon: Droplets,
      iconColor: "text-blue-400",
      iconBg: "bg-blue-500/15 border-blue-500/30",
      pill: "CGWB Network",
      pillColor: "bg-blue-500/10 text-blue-300 border-blue-500/25",
    },
    {
      title: "Contamination Hotspots",
      value: formatNumber(kpis.contaminatedWells + kpis.criticalRiskWells),
      description: "Exceeding safety thresholds (EC > 3000 µS/cm)",
      icon: AlertTriangle,
      iconColor: "text-rose-400",
      iconBg: "bg-rose-500/15 border-rose-500/30",
      pill: "Action Required",
      pillColor: "bg-rose-500/10 text-rose-300 border-rose-500/25",
    },
    {
      title: "Hydro-Geological Outliers",
      value: formatNumber(kpis.anomaliesDetected),
      description: "Wells deviating from their regional cluster norm",
      icon: Activity,
      iconColor: "text-violet-400",
      iconBg: "bg-violet-500/15 border-violet-500/30",
      pill: "Anomaly Flagged",
      pillColor: "bg-violet-500/10 text-violet-300 border-violet-500/25",
    },
    {
      title: "Monthly Testing Budget",
      value: `${kpis.pendingTestQueue} Kits`,
      description: "Smart allocation for lab verification this month",
      icon: Sparkles,
      iconColor: "text-indigo-400",
      iconBg: "bg-indigo-500/15 border-indigo-500/30",
      pill: "Active Learning",
      pillColor: "bg-indigo-500/10 text-indigo-300 border-indigo-500/25",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((c, i) => {
        const Icon = c.icon;
        return (
          <div
            key={i}
            className="rounded-2xl border border-white/8 bg-[#0D1526]/80 p-5 shadow-lg shadow-black/20 hover:border-white/15 backdrop-blur-md transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  {c.title}
                </span>
                <div
                  className={`flex h-8 w-8 items-center justify-center rounded-xl border ${c.iconBg} ${c.iconColor}`}
                >
                  <Icon className="h-4 w-4" />
                </div>
              </div>

              <div className="mt-3 flex items-baseline">
                <span className="text-2xl font-bold tracking-tight text-white font-mono">
                  {c.value}
                </span>
              </div>

              <p className="mt-1 text-xs text-slate-400 leading-snug">
                {c.description}
              </p>
            </div>

            <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs">
              <span
                className={`inline-flex items-center text-[10px] font-medium px-2.5 py-0.5 rounded-full border ${c.pillColor}`}
              >
                {c.pill}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
