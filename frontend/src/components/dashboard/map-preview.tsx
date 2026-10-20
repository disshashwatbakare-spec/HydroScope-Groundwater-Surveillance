"use client";

import * as React from "react";
import Link from "next/link";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MapPin, ExternalLink, Layers, ShieldCheck } from "lucide-react";
import { MOCK_WELLS } from "@/data/mock-wells";

export function MapPreview() {
  const [selectedWell, setSelectedWell] = React.useState(MOCK_WELLS[1]);

  return (
    <Card className="h-full flex flex-col shadow-lg shadow-black/20">
      <CardHeader className="p-5 pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-semibold text-white tracking-tight">
            Geospatial Hotspots Map
          </CardTitle>
          <Link href="/map">
            <Button variant="ghost" size="xs" className="h-7 text-xs text-blue-400 gap-1 hover:text-blue-300 hover:bg-white/5">
              <span>Open Full Map</span>
              <ExternalLink className="h-3 w-3" />
            </Button>
          </Link>
        </div>
        <CardDescription className="text-xs text-slate-400">
          Visual inspection of water quality risk and regional cluster boundaries across India
        </CardDescription>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col justify-between pt-0 pb-4">
        {/* Visual Map Surface */}
        <div className="relative h-60 w-full rounded-xl border border-white/8 bg-[#070C18] overflow-hidden flex items-center justify-center p-3">
          {/* Subtle grid pattern for cartographic look */}
          <div
            className="absolute inset-0 opacity-15"
            style={{
              backgroundImage:
                "radial-gradient(#38bdf8 0.75px, transparent 0.75px), radial-gradient(#38bdf8 0.75px, #070C18 0.75px)",
              backgroundSize: "24px 24px",
              backgroundPosition: "0 0, 12px 12px",
            }}
          />

          {/* India Boundary / Cluster Regions Mock overlay */}
          <svg className="absolute inset-0 h-full w-full" viewBox="0 0 500 300">
            {/* Cluster Hulls */}
            {/* Rajasthan Saline Rim (Cluster 1) */}
            <path
              d="M 120 70 Q 150 50 180 80 T 160 130 Z"
              fill="rgba(220, 38, 38, 0.12)"
              stroke="rgba(220, 38, 38, 0.5)"
              strokeWidth="1.2"
              strokeDasharray="3 3"
            />
            {/* Gujarat Coast & Kutch (Cluster 0) */}
            <path
              d="M 90 140 Q 130 130 150 170 T 110 200 Z"
              fill="rgba(245, 158, 11, 0.12)"
              stroke="rgba(245, 158, 11, 0.5)"
              strokeWidth="1.2"
              strokeDasharray="3 3"
            />
            {/* Maharashtra Basalt (Cluster 5 & 6) */}
            <path
              d="M 150 180 Q 210 160 250 200 T 180 240 Z"
              fill="rgba(59, 130, 246, 0.12)"
              stroke="rgba(59, 130, 246, 0.5)"
              strokeWidth="1.2"
              strokeDasharray="3 3"
            />
            {/* Andhra Krishna-Godavari (Cluster 2) */}
            <path
              d="M 260 210 Q 320 200 310 260 T 250 250 Z"
              fill="rgba(16, 185, 129, 0.12)"
              stroke="rgba(16, 185, 129, 0.5)"
              strokeWidth="1.2"
              strokeDasharray="3 3"
            />
            {/* West Bengal Alluvial (Cluster 8) */}
            <path
              d="M 370 140 Q 420 130 410 190 T 360 180 Z"
              fill="rgba(13, 148, 136, 0.12)"
              stroke="rgba(13, 148, 136, 0.5)"
              strokeWidth="1.2"
              strokeDasharray="3 3"
            />

            {/* Well points on the map */}
            {MOCK_WELLS.map((w, i) => {
              // Projected pseudo-coordinates for preview
              // Lon range: 69 to 89 -> X: 60 to 440
              // Lat range: 15 to 29 -> Y: 260 to 40
              const cx = 60 + ((w.longitude - 69) / 20) * 360;
              const cy = 260 - ((w.latitude - 15) / 14) * 210;

              const isSelected = selectedWell.id === w.id;
              const isCrit = w.riskLevel === "critical";
              const isHigh = w.riskLevel === "high";

              return (
                <g key={w.id} onClick={() => setSelectedWell(w)} className="cursor-pointer">
                  {w.isAnomaly && (
                    <circle
                      cx={cx}
                      cy={cy}
                      r={isSelected ? 10 : 7}
                      fill="none"
                      stroke="#c084fc"
                      strokeWidth="1.5"
                      opacity="0.8"
                    />
                  )}
                  <circle
                    cx={cx}
                    cy={cy}
                    r={isSelected ? 5 : isCrit ? 4 : 3}
                    fill={
                      isCrit
                        ? "#ef4444"
                        : isHigh
                        ? "#f59e0b"
                        : w.riskLevel === "medium"
                        ? "#38bdf8"
                        : "#34d399"
                    }
                    stroke="#ffffff"
                    strokeWidth={isSelected ? 2 : 1}
                  />
                </g>
              );
            })}
          </svg>

          {/* Quick HUD Selected Station Card */}
          <div className="absolute bottom-2.5 left-2.5 right-2.5 rounded-md border border-slate-700/80 bg-slate-900/90 p-2.5 backdrop-blur-xs text-xs text-white flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span
                className={`h-2.5 w-2.5 rounded-full ${
                  selectedWell.riskLevel === "critical"
                    ? "bg-red-500"
                    : selectedWell.riskLevel === "high"
                    ? "bg-amber-500"
                    : "bg-emerald-500"
                }`}
              />
              <div>
                <div className="font-semibold text-slate-100 flex items-center gap-1.5 text-[11px]">
                  <span>{selectedWell.station}</span>
                  <span className="text-slate-400 font-mono text-[10px]">
                    ({selectedWell.id})
                  </span>
                </div>
                <div className="text-[10px] text-slate-400 capitalize">
                  {selectedWell.district}, {selectedWell.state} | Cluster #{selectedWell.clusterDbscan}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3 text-right font-mono text-[11px]">
              <div>
                <div className="text-[9px] uppercase tracking-wider text-slate-400">
                  Conductivity
                </div>
                <div className="font-semibold text-amber-300">
                  {selectedWell.ecValue ? `${selectedWell.ecValue} µS/cm` : "Untested"}
                </div>
              </div>
              <div className="hidden sm:block">
                <div className="text-[9px] uppercase tracking-wider text-slate-400">
                  Risk Prob
                </div>
                <div className="font-semibold text-slate-100">
                  {selectedWell.contaminationProbability
                    ? `${(selectedWell.contaminationProbability * 100).toFixed(0)}%`
                    : "N/A"}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Legend */}
        <div className="mt-4 flex flex-wrap items-center justify-between text-[11px] text-slate-300 border-t border-white/5 pt-3">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-rose-500 shadow-xs shadow-rose-500/50" />
              Critical
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-amber-500 shadow-xs shadow-amber-500/50" />
              High
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-blue-400 shadow-xs shadow-blue-400/50" />
              Medium
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-emerald-500 shadow-xs shadow-emerald-500/50" />
              Low
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full border border-violet-400 bg-violet-500/30" />
              Cluster Anomaly
            </span>
          </div>

          <div className="text-slate-400 text-[10px]">
            Click points to inspect station
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
