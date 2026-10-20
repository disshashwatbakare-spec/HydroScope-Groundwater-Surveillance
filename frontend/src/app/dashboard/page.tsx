"use client";

import * as React from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import { KpiSummary } from "@/components/dashboard/kpi-summary";
import { RiskDistribution } from "@/components/dashboard/risk-distribution";
import { RegionalOverview } from "@/components/dashboard/regional-overview";
import { MapPreview } from "@/components/dashboard/map-preview";
import { PriorityWells } from "@/components/dashboard/priority-wells";
import { MOCK_KPIS } from "@/data/mock-wells";
import {
  MapPin,
  Droplets,
  ListOrdered,
  ArrowRight,
  Activity,
  AlertTriangle,
  CheckCircle2,
  BarChart3,
} from "lucide-react";

export default function DashboardPage() {
  return (
    <AppShell
      title="Surveillance Dashboard"
      subtitle="Groundwater Quality Monitoring & Smart Resource Allocation"
    >
      {/* Hero Banner */}
      <div
        className="relative overflow-hidden rounded-2xl p-6 shadow-sm border border-blue-900/20"
        style={{
          background: "linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f2d4a 100%)",
        }}
      >
        {/* Decorative grid overlay */}
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `radial-gradient(circle, #60a5fa 1px, transparent 1px)`,
            backgroundSize: "28px 28px",
          }}
        />
        {/* Glow blobs */}
        <div className="absolute -top-16 -right-16 w-64 h-64 rounded-full bg-blue-500/10 blur-3xl" />
        <div className="absolute -bottom-12 left-24 w-48 h-48 rounded-full bg-cyan-400/8 blur-3xl" />

        <div className="relative z-10 flex flex-wrap items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-emerald-400 text-xs font-semibold uppercase tracking-wider">
                Live Surveillance Active
              </span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              HydroScope
            </h2>
            <p className="text-blue-200/70 text-sm mt-1 max-w-sm">
              AI-powered groundwater contamination surveillance across 5 Indian states
            </p>
          </div>

          {/* Hero Stats Row */}
          <div className="flex flex-wrap items-center gap-4">
            <div className="text-center px-5 py-3 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
              <div className="text-2xl font-bold font-mono text-white">36,922</div>
              <div className="text-[11px] text-blue-200/60 mt-0.5 uppercase tracking-wide">Wells Monitored</div>
            </div>
            <div className="text-center px-5 py-3 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
              <div className="text-2xl font-bold font-mono text-red-300">5.59%</div>
              <div className="text-[11px] text-blue-200/60 mt-0.5 uppercase tracking-wide">Contaminated</div>
            </div>
            <div className="text-center px-5 py-3 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
              <div className="text-2xl font-bold font-mono text-amber-300">1,749</div>
              <div className="text-[11px] text-blue-200/60 mt-0.5 uppercase tracking-wide">Anomalies Flagged</div>
            </div>
            <div className="text-center px-5 py-3 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
              <div className="text-2xl font-bold font-mono text-emerald-300">0.894</div>
              <div className="text-[11px] text-blue-200/60 mt-0.5 uppercase tracking-wide">Model ROC-AUC</div>
            </div>
          </div>
        </div>
      </div>

      {/* 3 Core Feature Navigation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Feature 1: Geospatial Map */}
        <Link href="/map" className="group">
          <div className="h-full rounded-2xl border border-white/8 bg-[#0D1526]/80 p-5 shadow-lg shadow-black/20 transition-all duration-200 hover:border-blue-500/40 hover:bg-[#0D1526] hover:-translate-y-1 backdrop-blur-md">
            <div className="flex items-center justify-between">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30 shadow-sm shadow-blue-500/20 group-hover:scale-105 transition-transform">
                <MapPin className="h-5 w-5 text-blue-400" />
              </div>
              <span className="flex items-center gap-1 text-xs font-semibold text-blue-400 group-hover:text-blue-300 group-hover:translate-x-0.5 transition-all">
                Open Map <ArrowRight className="h-3.5 w-3.5" />
              </span>
            </div>
            <h3 className="mt-4 font-semibold text-white text-sm tracking-tight">
              Geospatial Risk Map
            </h3>
            <p className="mt-1.5 text-xs text-slate-400 leading-relaxed">
              Explore contamination clusters, water depth variations, and anomaly hotspots across all regions.
            </p>
            <div className="mt-4 flex items-center gap-1.5 pt-3 border-t border-white/5">
              <span className="h-1.5 w-1.5 rounded-full bg-blue-400 animate-pulse" />
              <span className="text-[10px] text-slate-400 font-medium">5 States · 39 DBSCAN Clusters</span>
            </div>
          </div>
        </Link>

        {/* Feature 2: Well Inventory */}
        <Link href="/wells" className="group">
          <div className="h-full rounded-2xl border border-white/8 bg-[#0D1526]/80 p-5 shadow-lg shadow-black/20 transition-all duration-200 hover:border-cyan-500/40 hover:bg-[#0D1526] hover:-translate-y-1 backdrop-blur-md">
            <div className="flex items-center justify-between">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-600/20 text-cyan-400 border border-cyan-500/30 shadow-sm shadow-cyan-500/20 group-hover:scale-105 transition-transform">
                <Droplets className="h-5 w-5 text-cyan-400" />
              </div>
              <span className="flex items-center gap-1 text-xs font-semibold text-cyan-400 group-hover:text-cyan-300 group-hover:translate-x-0.5 transition-all">
                Browse Wells <ArrowRight className="h-3.5 w-3.5" />
              </span>
            </div>
            <h3 className="mt-4 font-semibold text-white text-sm tracking-tight">
              Well Inventory
            </h3>
            <p className="mt-1.5 text-xs text-slate-400 leading-relaxed">
              Search, filter, and inspect 36,922 monitoring stations with historical records and ML scores.
            </p>
            <div className="mt-4 flex items-center gap-1.5 pt-3 border-t border-white/5">
              <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-pulse" />
              <span className="text-[10px] text-slate-400 font-medium">Sortable · Filterable · Exportable</span>
            </div>
          </div>
        </Link>

        {/* Feature 3: Active Testing Queue */}
        <Link href="/testing-queue" className="group">
          <div className="h-full rounded-2xl border border-white/8 bg-[#0D1526]/80 p-5 shadow-lg shadow-black/20 transition-all duration-200 hover:border-indigo-500/40 hover:bg-[#0D1526] hover:-translate-y-1 backdrop-blur-md">
            <div className="flex items-center justify-between">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30 shadow-sm shadow-indigo-500/20 group-hover:scale-105 transition-transform">
                <ListOrdered className="h-5 w-5 text-indigo-400" />
              </div>
              <span className="flex items-center gap-1 text-xs font-semibold text-indigo-400 group-hover:text-indigo-300 group-hover:translate-x-0.5 transition-all">
                View Queue <ArrowRight className="h-3.5 w-3.5" />
              </span>
            </div>
            <h3 className="mt-4 font-semibold text-white text-sm tracking-tight">
              Active Testing Queue
            </h3>
            <p className="mt-1.5 text-xs text-slate-400 leading-relaxed">
              Prioritise which wells receive lab testing kits within our 50 tests/month budget using BBN uncertainty.
            </p>
            <div className="mt-4 flex items-center gap-1.5 pt-3 border-t border-white/5">
              <span className="h-1.5 w-1.5 rounded-full bg-indigo-400 animate-pulse" />
              <span className="text-[10px] text-slate-400 font-medium">+86.4% Detection vs Random</span>
            </div>
          </div>
        </Link>
      </div>

      {/* KPI Cards Row */}
      <KpiSummary kpis={MOCK_KPIS} />

      {/* Primary Visual Section: Priority Wells + Map Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Priority Testing Action Queue (7 cols) */}
        <div className="lg:col-span-7">
          <PriorityWells />
        </div>

        {/* Geospatial Map Preview (5 cols) */}
        <div className="lg:col-span-5">
          <MapPreview />
        </div>
      </div>

      {/* Secondary: Regional Overview + Risk Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Regional Table (7 cols) */}
        <div className="lg:col-span-7">
          <RegionalOverview />
        </div>

        {/* Risk Distribution Donut (5 cols) */}
        <div className="lg:col-span-5">
          <RiskDistribution />
        </div>
      </div>
    </AppShell>
  );
}

