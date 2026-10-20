"use client";

import * as React from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { RiskBadge, ContaminationBadge, AnomalyBadge, DepthBadge } from "@/components/ui/badge";
import { MOCK_WELLS } from "@/data/mock-wells";
import type { Well, RiskLevel } from "@/types";
import {
  Layers,
  Search,
  MapPin,
  ExternalLink,
  Activity,
  Droplets,
  Calendar,
  AlertTriangle,
  Send,
  Eye,
  CheckCircle2,
} from "lucide-react";
import { formatNumber } from "@/lib/utils";

// Dynamic import with SSR disabled to prevent Leaflet window reference errors
const GroundwaterMap = dynamic(
  () => import("@/components/map/groundwater-map").then((mod) => mod.GroundwaterMap),
  {
    ssr: false,
    loading: () => (
      <div className="flex h-full w-full items-center justify-center bg-slate-100 text-xs text-slate-500 rounded-lg border border-slate-200">
        Initializing Cartographic GIS Engine...
      </div>
    ),
  }
);

export default function MapPage() {
  const [selectedWell, setSelectedWell] = React.useState<Well | null>(MOCK_WELLS[1]);
  const [search, setSearch] = React.useState("");
  const [selectedState, setSelectedState] = React.useState("all");
  const [selectedRisk, setSelectedRisk] = React.useState("all");
  const [showAnomaliesOnly, setShowAnomaliesOnly] = React.useState(false);

  const filteredWells = React.useMemo(() => {
    return MOCK_WELLS.filter((w) => {
      if (search) {
        const q = search.toLowerCase();
        if (
          !w.station.toLowerCase().includes(q) &&
          !w.id.toLowerCase().includes(q) &&
          !w.district.toLowerCase().includes(q)
        ) {
          return false;
        }
      }
      if (selectedState !== "all" && w.state.toLowerCase() !== selectedState.toLowerCase()) {
        return false;
      }
      if (selectedRisk !== "all" && w.riskLevel !== selectedRisk) {
        return false;
      }
      if (showAnomaliesOnly && !w.isAnomaly) {
        return false;
      }
      return true;
    });
  }, [search, selectedState, selectedRisk, showAnomaliesOnly]);

  return (
    <AppShell
      title="Geospatial Groundwater Risk Map"
      subtitle="Interactive Cluster Topography, Infiltration Vulnerability & Anomaly Hotspots"
    >
      {/* Top Filter Bar */}
      <Card className="p-3 shadow-2xs">
        <div className="flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative w-56">
              <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-400" />
              <Input
                placeholder="Find station or district..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-8 h-8 text-xs"
              />
            </div>

            <Select
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="h-8 text-xs"
            >
              <option value="all">All States</option>
              <option value="maharashtra">Maharashtra</option>
              <option value="andhra pradesh">Andhra Pradesh</option>
              <option value="west bengal">West Bengal</option>
              <option value="rajasthan">Rajasthan</option>
              <option value="gujarat">Gujarat</option>
            </Select>

            <Select
              value={selectedRisk}
              onChange={(e) => setSelectedRisk(e.target.value)}
              className="h-8 text-xs"
            >
              <option value="all">All Risk Tiers</option>
              <option value="critical">Critical Risk</option>
              <option value="high">High Risk</option>
              <option value="medium">Medium Risk</option>
              <option value="low">Low Risk</option>
            </Select>

            <Button
              variant={showAnomaliesOnly ? "primary" : "outline"}
              size="xs"
              onClick={() => setShowAnomaliesOnly(!showAnomaliesOnly)}
              className="h-8 text-xs gap-1"
            >
              <AlertTriangle className="h-3 w-3" />
              <span>Anomalies Only ({MOCK_WELLS.filter((w) => w.isAnomaly).length})</span>
            </Button>
          </div>

          <div className="flex items-center gap-3 font-mono text-[11px] text-slate-400">
            <span>
              Active Pins: <strong className="text-white font-semibold">{filteredWells.length}</strong> / {MOCK_WELLS.length}
            </span>
          </div>
        </div>
      </Card>

      {/* Main Map + Side Panel Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 h-[640px]">
        {/* Map View (8 cols) */}
        <div className="lg:col-span-8 h-full flex flex-col">
          <GroundwaterMap
            wells={filteredWells}
            selectedWell={selectedWell}
            onSelectWell={setSelectedWell}
            showAnomaliesOnly={showAnomaliesOnly}
            showClusters={true}
          />
        </div>

        {/* Selected Well HUD & Station List (4 cols) */}
        <div className="lg:col-span-4 h-full flex flex-col gap-4">
          {/* Station Details Card */}
          {selectedWell ? (
            <Card className="p-5 shadow-lg shadow-black/20 space-y-3.5">
              <div className="flex items-center justify-between border-b border-white/8 pb-3">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-bold text-sm text-white">
                      {selectedWell.station}
                    </h3>
                    <span className="font-mono text-[10px] text-slate-300 bg-white/5 border border-white/10 px-2 py-0.5 rounded-full">
                      {selectedWell.id}
                    </span>
                  </div>
                  <div className="text-[11px] text-slate-400 capitalize mt-0.5">
                    {selectedWell.district}, {selectedWell.state}
                  </div>
                </div>
                <RiskBadge level={selectedWell.riskLevel} />
              </div>

              {/* Coordinates & Depth */}
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
                  <div className="text-[10px] text-slate-400 uppercase tracking-wider">Conductivity</div>
                  <div className="font-mono font-bold text-white mt-1">
                    {selectedWell.ecValue ? `${formatNumber(selectedWell.ecValue)} µS/cm` : "Untested"}
                  </div>
                </div>

                <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
                  <div className="text-[10px] text-slate-400 uppercase tracking-wider">Water Depth</div>
                  <div className="font-mono font-bold text-white mt-1">
                    {selectedWell.groundwaterLevelM?.toFixed(1) || "?"} m ({selectedWell.gwDepthCategory})
                  </div>
                </div>

                <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
                  <div className="text-[10px] text-slate-400 uppercase tracking-wider">ML Risk Prob</div>
                  <div className="font-mono font-bold text-white mt-1">
                    {selectedWell.contaminationProbability
                      ? `${(selectedWell.contaminationProbability * 100).toFixed(0)}%`
                      : "N/A"}
                  </div>
                </div>

                <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
                  <div className="text-[10px] text-slate-400 uppercase tracking-wider">DBSCAN Cluster</div>
                  <div className="font-mono font-bold text-white mt-1">
                    Cluster #{selectedWell.clusterDbscan}
                  </div>
                </div>
              </div>

              {/* Anomaly Callout */}
              {selectedWell.isAnomaly && (
                <div className="rounded-xl bg-violet-500/15 p-3 text-[11px] text-violet-300 border border-violet-500/30">
                  <strong className="block mb-0.5 text-violet-200">Within-Cluster Isolation Forest Anomaly</strong>
                  Station deviates from regional cluster norm (Score: {selectedWell.anomalyScore?.toFixed(2)}).
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-3 border-t border-white/8">
                <Link href={`/wells/${selectedWell.id}`}>
                  <Button variant="outline" size="xs" className="h-8 text-xs gap-1.5 border-white/15 text-slate-200 hover:text-white">
                    <span>Full Analysis</span>
                    <ExternalLink className="h-3 w-3" />
                  </Button>
                </Link>

                <Link href="/testing-queue">
                  <Button variant="primary" size="xs" className="h-8 text-xs gap-1.5 bg-blue-600 hover:bg-blue-500 text-white shadow-sm shadow-blue-500/20">
                    <Send className="h-3 w-3" />
                    <span>Prioritize Testing</span>
                  </Button>
                </Link>
              </div>
            </Card>
          ) : (
            <Card className="p-5 shadow-lg shadow-black/20 text-center text-xs text-slate-400">
              Click any well point on the map to inspect telemetry and causal drivers.
            </Card>
          )}

          {/* Station List Card */}
          <Card className="flex-1 flex flex-col overflow-hidden shadow-lg shadow-black/20">
            <CardHeader className="p-4 pb-2.5 border-b border-white/8">
              <CardTitle className="text-xs text-white">Surveillance Stations ({filteredWells.length})</CardTitle>
            </CardHeader>
            <div className="flex-1 overflow-y-auto divide-y divide-white/5 p-1.5">
              {filteredWells.map((w) => {
                const isSelected = selectedWell?.id === w.id;
                return (
                  <button
                    key={w.id}
                    onClick={() => setSelectedWell(w)}
                    className={`w-full text-left p-2.5 rounded-xl transition-all text-xs flex items-center justify-between cursor-pointer ${
                      isSelected ? "bg-white/10 text-white font-semibold border border-white/10" : "hover:bg-white/5 text-slate-300"
                    }`}
                  >
                    <div>
                      <div className="text-white text-xs truncate max-w-[170px]">
                        {w.station}
                      </div>
                      <div className="text-[10px] text-slate-400 capitalize">
                        {w.district}, {w.state}
                      </div>
                    </div>
                    <div className="flex items-center gap-1.5">
                      {w.isAnomaly && (
                        <span className="h-1.5 w-1.5 rounded-full bg-violet-400" />
                      )}
                      <span
                        className={`text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full border ${
                          w.riskLevel === "critical"
                            ? "bg-rose-500/15 text-rose-300 border-rose-500/30"
                            : w.riskLevel === "high"
                            ? "bg-amber-500/15 text-amber-300 border-amber-500/30"
                            : "bg-emerald-500/15 text-emerald-300 border-emerald-500/30"
                        }`}
                      >
                        {w.contaminationProbability
                          ? `${(w.contaminationProbability * 100).toFixed(0)}%`
                          : "N/A"}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
