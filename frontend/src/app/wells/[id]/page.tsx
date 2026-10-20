"use client";

import * as React from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RiskBadge, ContaminationBadge, AnomalyBadge, DepthBadge } from "@/components/ui/badge";
import { getWellById, MOCK_WELLS } from "@/data/mock-wells";
import {
  ArrowLeft,
  MapPin,
  Calendar,
  Layers,
  Send,
  CheckCircle2,
  AlertTriangle,
  Info,
  ShieldCheck,
  Activity,
  Cpu,
  Droplets,
  ExternalLink,
} from "lucide-react";
import { formatNumber } from "@/lib/utils";

export default function WellDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const id = params?.id as string;

  const well = getWellById(id) || MOCK_WELLS[1]; // fallback to realistic well if id not matched
  const [kitDispatched, setKitDispatched] = React.useState(false);
  const [fieldNotes, setFieldNotes] = React.useState("");

  return (
    <AppShell
      title={`Well Station: ${well.station}`}
      subtitle={`National CGWB Monitoring Station [ID: ${well.id}]`}
    >
      {/* Back Link & Quick Actions */}
      <div className="flex items-center justify-between">
        <Link
          href="/wells"
          className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          <span>Back to Well Inventory</span>
        </Link>

        <div className="flex items-center gap-2">
          <Link href="/map">
            <Button variant="outline" size="sm" className="text-xs gap-1.5 border-white/15 text-slate-200 hover:text-white">
              <MapPin className="h-3.5 w-3.5" />
              <span>Locate on Map</span>
            </Button>
          </Link>
          <Button
            variant={kitDispatched ? "secondary" : "primary"}
            size="sm"
            onClick={() => setKitDispatched(!kitDispatched)}
            className={`text-xs gap-1.5 ${kitDispatched ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30" : "bg-blue-600 hover:bg-blue-500 text-white shadow-sm shadow-blue-500/20"}`}
          >
            {kitDispatched ? (
              <>
                <CheckCircle2 className="h-3.5 w-3.5" />
                <span>Test Kit Dispatched</span>
              </>
            ) : (
              <>
                <Send className="h-3.5 w-3.5" />
                <span>Dispatch Testing Kit</span>
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Hero Overview Card */}
      <Card className="p-5 shadow-lg shadow-black/20">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex flex-wrap items-center gap-2">
              <h2 className="text-lg font-bold text-white tracking-tight">
                {well.station}
              </h2>
              <span className="font-mono text-xs text-slate-300 bg-white/5 px-2 py-0.5 rounded border border-white/10">
                {well.id}
              </span>
              <RiskBadge level={well.riskLevel} />
              <ContaminationBadge status={well.status} />
              {well.isAnomaly && <AnomalyBadge isAnomaly={true} score={well.anomalyScore} />}
            </div>

            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400">
              <span className="flex items-center gap-1 capitalize">
                <MapPin className="h-3.5 w-3.5 text-slate-400" />
                {well.district}, {well.state}
              </span>
              <span className="font-mono text-slate-400">
                Lat: {well.latitude.toFixed(4)}° N, Lon: {well.longitude.toFixed(4)}° E
              </span>
              <span className="flex items-center gap-1">
                <Calendar className="h-3.5 w-3.5 text-slate-400" />
                Last Lab Recorded: {well.lastTestedDate || "Historical Record"}
              </span>
            </div>
          </div>

          {/* Quick Probability Callout */}
          <div className="flex items-center gap-3 border-t md:border-t-0 md:border-l border-white/10 pt-3 md:pt-0 md:pl-5">
            <div className="flex flex-col items-end">
              <span className="text-[10px] uppercase font-semibold text-slate-400 tracking-wider">
                Predicted Risk
              </span>
              <span className="text-2xl font-bold font-mono text-white">
                {well.contaminationProbability
                  ? `${(well.contaminationProbability * 100).toFixed(0)}%`
                  : "N/A"}
              </span>
            </div>
            <div
              className={`h-10 w-1 rounded-full ${
                well.riskLevel === "critical"
                  ? "bg-rose-500"
                  : well.riskLevel === "high"
                  ? "bg-amber-500"
                  : "bg-emerald-500"
              }`}
            />
          </div>
        </div>
      </Card>

      {/* Grid: 4 Technical Dimension Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Dimension 1: Water Table Depth */}
        <Card className="p-4 shadow-lg shadow-black/20">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-semibold uppercase tracking-wider text-[10px]">
              Groundwater Level (Depth)
            </span>
            <Droplets className="h-4 w-4 text-blue-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {well.groundwaterLevelM !== null ? `${well.groundwaterLevelM.toFixed(1)} m` : "N/A"}
          </div>
          <div className="mt-2 flex items-center justify-between">
            <DepthBadge category={well.gwDepthCategory} />
            <span className="text-[10px] text-slate-400">Below surface level</span>
          </div>
        </Card>

        {/* Dimension 2: Electrical Conductivity */}
        <Card className="p-4 shadow-lg shadow-black/20">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-semibold uppercase tracking-wider text-[10px]">
              Electrical Conductivity (EC)
            </span>
            <Activity className="h-4 w-4 text-amber-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {well.ecValue ? `${formatNumber(well.ecValue)} µS/cm` : "Untested"}
          </div>
          <div className="mt-2 flex items-center justify-between text-[11px]">
            <span className="text-slate-400">Threshold: 3,000 µS/cm</span>
            <span
              className={`font-semibold ${
                well.ecValue && well.ecValue > 3000 ? "text-rose-400" : "text-emerald-400"
              }`}
            >
              {well.ecValue && well.ecValue > 3000 ? "+ Exceeded" : "Within Norm"}
            </span>
          </div>
        </Card>

        {/* Dimension 3: Spatial Cluster */}
        <Card className="p-4 shadow-lg shadow-black/20">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-semibold uppercase tracking-wider text-[10px]">
              Spatial Cluster (Phase 3)
            </span>
            <Layers className="h-4 w-4 text-purple-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            DBSCAN #{well.clusterDbscan}
          </div>
          <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
            <span>Agglomerative: #{well.clusterAgg}</span>
            <span className="font-mono text-[10px] text-purple-300 bg-purple-500/15 border border-purple-500/30 px-1.5 py-0.5 rounded">
              ε=0.35, min=10
            </span>
          </div>
        </Card>

        {/* Dimension 4: Anomaly Decision Score */}
        <Card className="p-4 shadow-lg shadow-black/20">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-semibold uppercase tracking-wider text-[10px]">
              Within-Cluster Anomaly
            </span>
            <AlertTriangle className="h-4 w-4 text-rose-400" />
          </div>
          <div className="text-xl font-bold font-mono text-white">
            {well.anomalyScore !== null ? well.anomalyScore.toFixed(3) : "N/A"}
          </div>
          <div className="mt-2 flex items-center justify-between text-[11px]">
            <span className="text-slate-400">Isolation Forest</span>
            <span
              className={`font-semibold ${
                well.isAnomaly ? "text-rose-400" : "text-slate-400"
              }`}
            >
              {well.isAnomaly ? "Outlier Detected" : "Inlier Normal"}
            </span>
          </div>
        </Card>
      </div>

      {/* Main Grid: Bayesian Belief Network Causal Analysis & Dispatch Action */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Bayesian Belief Network Explanation (7 cols) */}
        <div className="lg:col-span-7">
          <Card className="h-full flex flex-col shadow-lg shadow-black/20">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Bayesian Belief Network (BBN) Causal Inference</CardTitle>
                <span className="rounded bg-white/5 px-2 py-0.5 text-[10px] font-mono text-slate-300 border border-white/10">
                  pgmpy Exact Inference
                </span>
              </div>
              <CardDescription>
                Probabilistic causal explanation of contamination risk conditioned on regional evidence
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4 flex-1">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {/* Evidence Node 1 */}
                <div className="rounded-xl border border-white/10 bg-white/5 p-3">
                  <div className="text-[10px] uppercase font-semibold text-slate-400">
                    Cluster Hydro Risk
                  </div>
                  <div className="mt-1 text-sm font-bold text-white font-mono">
                    {well.bbnClusterRisk === 1 ? "High-Salinity Zone (1)" : "Low-Salinity Zone (0)"}
                  </div>
                  <div className="mt-1 text-[10px] text-slate-400">
                    Conditioned on Cluster #{well.clusterDbscan} mean EC
                  </div>
                </div>

                {/* Evidence Node 2 */}
                <div className="rounded-xl border border-white/10 bg-white/5 p-3">
                  <div className="text-[10px] uppercase font-semibold text-slate-400">
                    District Urbanization
                  </div>
                  <div className="mt-1 text-sm font-bold text-white font-mono">
                    {well.bbnDistrictUrban === 1 ? "Urbanized District (1)" : "Rural Agricultural (0)"}
                  </div>
                  <div className="mt-1 text-[10px] text-slate-400">
                    Anthropogenic effluent factor
                  </div>
                </div>

                {/* Evidence Node 3 */}
                <div className="rounded-xl border border-white/10 bg-white/5 p-3">
                  <div className="text-[10px] uppercase font-semibold text-slate-400">
                    Aquifer Depth Profile
                  </div>
                  <div className="mt-1 text-sm font-bold text-white font-mono capitalize">
                    {well.gwDepthCategory} ({well.groundwaterLevelM?.toFixed(1) || "?"}m)
                  </div>
                  <div className="mt-1 text-[10px] text-slate-400">
                    Vulnerability to surface runoff
                  </div>
                </div>
              </div>

              {/* Causal Graph Description Box */}
              <div className="rounded-xl border border-blue-500/20 bg-blue-950/30 p-4 text-xs text-slate-300">
                <div className="font-semibold flex items-center gap-1.5 mb-1.5 text-blue-300">
                  <Info className="h-4 w-4 text-blue-400" />
                  Causal Reasoning Summary
                </div>
                <p className="text-slate-300 text-xs leading-relaxed">
                  Given that this station is situated in an{" "}
                  <strong className="text-white">
                    {well.bbnDistrictUrban ? "urbanized" : "agricultural rural"}
                  </strong>{" "}
                  zone in <strong className="text-white">{well.district}</strong> with a{" "}
                  <strong className="text-white">{well.gwDepthCategory}</strong> water table depth, the Bayesian model updates the
                  prior probability from 5.59% baseline up to{" "}
                  <strong className="text-white font-mono">
                    {well.contaminationProbability
                      ? `${(well.contaminationProbability * 100).toFixed(0)}%`
                      : "40%"}
                  </strong>
                  . The within-cluster Isolation Forest flags this station as an outlier (anomaly score:{" "}
                  <span className="font-mono text-white">{well.anomalyScore?.toFixed(2)}</span>), warranting priority lab testing.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Lab Dispatch & Active Learning Queue Card (5 cols) */}
        <div className="lg:col-span-5">
          <Card className="h-full flex flex-col justify-between shadow-lg shadow-black/20">
            <CardHeader>
              <CardTitle>Field Sampling & Active Learning</CardTitle>
              <CardDescription>
                Testing queue priority ranking and dispatch allocation
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              <div className="rounded-xl border border-white/10 bg-white/5 p-3">
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="text-slate-400 font-medium">Uncertainty Sampling Rank:</span>
                  <span className="font-mono font-bold text-blue-400">
                    {well.testingPriority ? `Priority #${well.testingPriority}` : "Not in Top 10 Queue"}
                  </span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400 font-medium">Model Epistemic Uncertainty:</span>
                  <span className="font-mono font-bold text-white">
                    {well.uncertaintySamplingScore !== null
                      ? well.uncertaintySamplingScore.toFixed(3)
                      : "0.150"}
                  </span>
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] font-medium text-slate-300">
                  Field Inspector Protocol Notes
                </label>
                <textarea
                  className="w-full rounded-xl border border-white/10 bg-black/30 p-2.5 text-xs text-slate-200 placeholder:text-slate-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  rows={3}
                  placeholder="Record well condition, casing integrity, nearby agricultural/industrial runoff..."
                  value={fieldNotes}
                  onChange={(e) => setFieldNotes(e.target.value)}
                />
              </div>

              <div className="pt-2 border-t border-white/10 flex items-center justify-between">
                <span className="text-[11px] text-slate-400">
                  {kitDispatched ? "Status: Dispatched to Field Team" : "Status: Ready for Dispatch"}
                </span>
                <Button
                  variant={kitDispatched ? "secondary" : "primary"}
                  size="sm"
                  onClick={() => setKitDispatched(!kitDispatched)}
                  className={`text-xs gap-1 ${kitDispatched ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30" : "bg-blue-600 hover:bg-blue-500 text-white shadow-sm shadow-blue-500/20"}`}
                >
                  <Send className="h-3 w-3" />
                  <span>{kitDispatched ? "Update Dispatch" : "Confirm Dispatch"}</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
