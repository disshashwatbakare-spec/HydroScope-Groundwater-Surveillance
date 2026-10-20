"use client";

import * as React from "react";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  BarChart,
  Bar,
} from "recharts";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import {
  BarChart3,
  TrendingUp,
  Cpu,
  Layers,
  ShieldAlert,
  Info,
  Sliders,
  DollarSign,
  Award,
} from "lucide-react";

// Realistic curves calculated from HydroScope Phase 2 classifier evaluations
const ROC_CURVE_DATA = [
  { fpr: 0.0, rf: 0.0, adaboost: 0.0, knn: 0.0, baseline: 0.0 },
  { fpr: 0.05, rf: 0.62, adaboost: 0.54, knn: 0.42, baseline: 0.05 },
  { fpr: 0.1, rf: 0.78, adaboost: 0.71, knn: 0.58, baseline: 0.1 },
  { fpr: 0.15, rf: 0.85, adaboost: 0.8, knn: 0.69, baseline: 0.15 },
  { fpr: 0.2, rf: 0.89, adaboost: 0.84, knn: 0.75, baseline: 0.2 },
  { fpr: 0.3, rf: 0.93, adaboost: 0.89, knn: 0.81, baseline: 0.3 },
  { fpr: 0.4, rf: 0.95, adaboost: 0.92, knn: 0.86, baseline: 0.4 },
  { fpr: 0.5, rf: 0.97, adaboost: 0.94, knn: 0.9, baseline: 0.5 },
  { fpr: 0.7, rf: 0.99, adaboost: 0.98, knn: 0.96, baseline: 0.7 },
  { fpr: 1.0, rf: 1.0, adaboost: 1.0, knn: 1.0, baseline: 1.0 },
];

const COST_BENEFIT_DATA = [
  { threshold: 0.1, totalCost: 14200, fnCost: 1200, fpCost: 13000 },
  { threshold: 0.2, totalCost: 8900, fnCost: 2600, fpCost: 6300 },
  { threshold: 0.3, totalCost: 6100, fnCost: 3800, fpCost: 2300 },
  { threshold: 0.35, totalCost: 5450, fnCost: 4200, fpCost: 1250 }, // Optimal minimal cost
  { threshold: 0.4, totalCost: 5900, fnCost: 5100, fpCost: 800 },
  { threshold: 0.5, totalCost: 7800, fnCost: 7400, fpCost: 400 },
  { threshold: 0.6, totalCost: 11200, fnCost: 11000, fpCost: 200 },
  { threshold: 0.7, totalCost: 15600, fnCost: 15500, fpCost: 100 },
];

const FEATURE_IMPORTANCE = [
  { feature: "Electrical Conductivity (EC)", importance: 0.384, category: "Chemical" },
  { feature: "Groundwater Level (GWL Depth)", importance: 0.241, category: "Physical" },
  { feature: "District Hydro-Geological Code", importance: 0.162, category: "Geospatial" },
  { feature: "Latitude (Spatial)", importance: 0.118, category: "Geospatial" },
  { feature: "Longitude (Spatial)", importance: 0.095, category: "Geospatial" },
];

export default function AnalyticsPage() {
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <AppShell
      title="Machine Learning Performance & Metrics"
      subtitle="Phase 2 Imbalance Handling (SMOTE), Classifier Evaluation & Cost-Benefit Analysis"
    >
      {/* Top Model Benchmark Scorecards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Model 1: Random Forest + SMOTE */}
        <Card className="p-5 shadow-lg shadow-black/20 border-blue-500/30 bg-[#0D1526]/80 relative">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-semibold uppercase tracking-wider text-[10px] text-blue-400">
              Primary Model
            </span>
            <span className="rounded-full bg-blue-500/15 px-2.5 py-0.5 text-[10px] font-bold text-blue-300 border border-blue-500/30">
              Production
            </span>
          </div>
          <div className="text-sm font-bold text-white tracking-tight">
            Random Forest + SMOTE
          </div>
          <div className="mt-3.5 grid grid-cols-2 gap-2 text-xs">
            <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">ROC-AUC</span>
              <div className="font-mono font-bold text-lg text-white mt-0.5">0.9217</div>
            </div>
            <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Avg Precision</span>
              <div className="font-mono font-bold text-lg text-white mt-0.5">0.5683</div>
            </div>
          </div>
        </Card>

        {/* Model 2: AdaBoost + SMOTE */}
        <Card className="p-5 shadow-lg shadow-black/20 bg-[#0D1526]/80">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-semibold uppercase tracking-wider text-[10px]">
              Ensemble Comparison
            </span>
            <span className="text-[10px] text-slate-400 font-mono">150 Estimators</span>
          </div>
          <div className="text-sm font-bold text-white tracking-tight">
            AdaBoost + SMOTE
          </div>
          <div className="mt-3.5 grid grid-cols-2 gap-2 text-xs">
            <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">ROC-AUC</span>
              <div className="font-mono font-bold text-lg text-white mt-0.5">0.8620</div>
            </div>
            <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Avg Precision</span>
              <div className="font-mono font-bold text-lg text-white mt-0.5">0.8030</div>
            </div>
          </div>
        </Card>

        {/* Model 3: KNN Baseline */}
        <Card className="p-5 shadow-lg shadow-black/20 bg-[#0D1526]/80">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="font-semibold uppercase tracking-wider text-[10px]">
              Unbalanced Baseline
            </span>
            <span className="text-[10px] text-slate-400 font-mono">k = 7</span>
          </div>
          <div className="text-sm font-bold text-white tracking-tight">
            K-Nearest Neighbours (KNN)
          </div>
          <div className="mt-3.5 grid grid-cols-2 gap-2 text-xs">
            <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">ROC-AUC</span>
              <div className="font-mono font-bold text-lg text-white mt-0.5">0.7810</div>
            </div>
            <div className="rounded-xl border border-white/8 bg-white/5 p-2.5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Avg Precision</span>
              <div className="font-mono font-bold text-lg text-white mt-0.5">0.7120</div>
            </div>
          </div>
        </Card>
      </div>

      {/* Main Grid: ROC Curves & Cost Benefit Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* ROC Comparison Chart (7 cols) */}
        <div className="lg:col-span-7">
          <Card className="h-full flex flex-col shadow-lg shadow-black/20">
            <CardHeader className="p-5 pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm font-semibold text-white tracking-tight">Receiver Operating Characteristic (ROC) Curves</CardTitle>
                <span className="text-[11px] font-mono text-slate-300 bg-white/5 border border-white/10 px-2.5 py-0.5 rounded-full">
                  Test Set N=7,385
                </span>
              </div>
              <CardDescription className="text-xs text-slate-400">
                True Positive Rate vs False Positive Rate across decision thresholds
              </CardDescription>
            </CardHeader>

            <CardContent className="h-80 w-full pt-4">
              {mounted ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={ROC_CURVE_DATA} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis
                      dataKey="fpr"
                      stroke="#64748b"
                      tickFormatter={(v) => v.toFixed(2)}
                      label={{ value: "False Positive Rate (FPR)", position: "insideBottom", offset: -5, fontSize: 11, fill: "#94a3b8" }}
                      tick={{ fontSize: 11, fill: "#94a3b8" }}
                    />
                    <YAxis
                      stroke="#64748b"
                      tickFormatter={(v) => v.toFixed(2)}
                      label={{ value: "True Positive Rate (TPR)", angle: -90, position: "insideLeft", fontSize: 11, fill: "#94a3b8" }}
                      tick={{ fontSize: 11, fill: "#94a3b8" }}
                    />
                    <Tooltip
                      formatter={(val: any, name: any) => [`${(Number(val) * 100).toFixed(1)}%`, name]}
                      labelFormatter={(lbl) => `FPR: ${Number(lbl).toFixed(2)}`}
                      contentStyle={{
                        backgroundColor: "#0D1526",
                        borderColor: "rgba(255,255,255,0.15)",
                        borderRadius: "12px",
                        fontSize: "11px",
                        color: "#ffffff",
                        boxShadow: "0 8px 16px rgba(0,0,0,0.4)",
                      }}
                      itemStyle={{ color: "#ffffff" }}
                    />
                    <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px", color: "#94a3b8" }} />
                    <Line
                      type="monotone"
                      dataKey="rf"
                      name="Random Forest + SMOTE (0.92)"
                      stroke="#3B82F6"
                      strokeWidth={2.5}
                      dot={{ r: 3, fill: "#3B82F6" }}
                    />
                    <Line
                      type="monotone"
                      dataKey="adaboost"
                      name="AdaBoost + SMOTE (0.86)"
                      stroke="#06B6D4"
                      strokeWidth={1.8}
                      dot={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="knn"
                      name="KNN Baseline (0.78)"
                      stroke="#94a3b8"
                      strokeWidth={1.5}
                      strokeDasharray="4 4"
                      dot={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="baseline"
                      name="Chance (0.50)"
                      stroke="#475569"
                      strokeWidth={1}
                      strokeDasharray="2 2"
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex h-full items-center justify-center text-xs text-slate-400">
                  Loading curves...
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Cost-Benefit Curve (5 cols) */}
        <div className="lg:col-span-5">
          <Card className="h-full flex flex-col shadow-lg shadow-black/20">
            <CardHeader className="p-5 pb-2">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm font-semibold text-white tracking-tight">Cost-Benefit Analysis Curve</CardTitle>
                <span className="rounded-full bg-amber-500/15 px-2.5 py-0.5 text-[10px] font-semibold text-amber-300 border border-amber-500/30">
                  Optimal Threshold = 0.35
                </span>
              </div>
              <CardDescription className="text-xs text-slate-400">
                Minimises: (FN × 100) + (FP × 10) — Missing contamination penalized 10x
              </CardDescription>
            </CardHeader>

            <CardContent className="h-80 w-full pt-4">
              {mounted ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={COST_BENEFIT_DATA} margin={{ top: 10, right: 15, left: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis
                      dataKey="threshold"
                      stroke="#64748b"
                      label={{ value: "Decision Threshold", position: "insideBottom", offset: -5, fontSize: 11, fill: "#94a3b8" }}
                      tick={{ fontSize: 11, fill: "#94a3b8" }}
                    />
                    <YAxis
                      stroke="#64748b"
                      tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`}
                      label={{ value: "Total Cost Units", angle: -90, position: "insideLeft", fontSize: 11, fill: "#94a3b8" }}
                      tick={{ fontSize: 11, fill: "#94a3b8" }}
                    />
                    <Tooltip
                      formatter={(val: any, name: any) => [`${Number(val).toLocaleString()} Units`, name]}
                      labelFormatter={(lbl) => `Threshold: ${lbl}`}
                      contentStyle={{
                        backgroundColor: "#0D1526",
                        borderColor: "rgba(255,255,255,0.15)",
                        borderRadius: "12px",
                        fontSize: "11px",
                        color: "#ffffff",
                        boxShadow: "0 8px 16px rgba(0,0,0,0.4)",
                      }}
                      itemStyle={{ color: "#ffffff" }}
                    />
                    <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px", color: "#94a3b8" }} />
                    <Line
                      type="monotone"
                      dataKey="totalCost"
                      name="Total Health & Testing Cost"
                      stroke="#EF4444"
                      strokeWidth={2.5}
                      dot={{ r: 4, fill: "#EF4444" }}
                    />
                    <Line
                      type="monotone"
                      dataKey="fnCost"
                      name="False Negative Penalty (Health Risk)"
                      stroke="#F59E0B"
                      strokeWidth={1.5}
                      strokeDasharray="3 3"
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex h-full items-center justify-center text-xs text-slate-400">
                  Loading cost model...
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Feature Importance & Confusion Matrix Row */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Feature Importance (7 cols) */}
        <div className="lg:col-span-7">
          <Card className="shadow-lg shadow-black/20">
            <CardHeader className="p-5 pb-2">
              <CardTitle className="text-sm font-semibold text-white tracking-tight">Feature Importance (Random Forest Gini Impurity)</CardTitle>
              <CardDescription className="text-xs text-slate-400">
                Primary predictive drivers in rural groundwater contamination classification
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3.5 p-5 pt-3">
              {FEATURE_IMPORTANCE.map((f, i) => (
                <div key={i} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-white">{f.feature}</span>
                    <span className="font-mono text-blue-400 font-medium">
                      {(f.importance * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-white/10 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-blue-500 h-full rounded-full transition-all duration-300"
                      style={{ width: `${f.importance * 220}%` }}
                    />
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Confusion Matrix (5 cols) */}
        <div className="lg:col-span-5">
          <Card className="shadow-lg shadow-black/20 h-full flex flex-col justify-between">
            <CardHeader className="p-5 pb-2">
              <CardTitle className="text-sm font-semibold text-white tracking-tight">Confusion Matrix (Optimal Threshold 0.35)</CardTitle>
              <CardDescription className="text-xs text-slate-400">
                Evaluated on held-out test split (20% stratified sample)
              </CardDescription>
            </CardHeader>

            <CardContent className="p-5 pt-3">
              <div className="grid grid-cols-2 gap-3 text-center">
                <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3.5">
                  <div className="text-[10px] uppercase font-bold text-emerald-300 tracking-wider">
                    True Negatives (TN)
                  </div>
                  <div className="text-xl font-bold font-mono text-white mt-1">
                    6,842
                  </div>
                  <div className="text-[10px] text-slate-400 mt-0.5">Clean wells correctly verified</div>
                </div>

                <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 p-3.5">
                  <div className="text-[10px] uppercase font-bold text-amber-300 tracking-wider">
                    False Positives (FP)
                  </div>
                  <div className="text-xl font-bold font-mono text-white mt-1">
                    125
                  </div>
                  <div className="text-[10px] text-slate-400 mt-0.5">Tested clean unnecessarily</div>
                </div>

                <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-3.5">
                  <div className="text-[10px] uppercase font-bold text-rose-300 tracking-wider">
                    False Negatives (FN)
                  </div>
                  <div className="text-xl font-bold font-mono text-white mt-1">
                    42
                  </div>
                  <div className="text-[10px] text-slate-400 mt-0.5">Missed contamination (Penalty)</div>
                </div>

                <div className="rounded-xl border border-blue-500/30 bg-blue-500/10 p-3.5">
                  <div className="text-[10px] uppercase font-bold text-blue-300 tracking-wider">
                    True Positives (TP)
                  </div>
                  <div className="text-xl font-bold font-mono text-white mt-1">
                    376
                  </div>
                  <div className="text-[10px] text-slate-400 mt-0.5">Contaminated wells discovered</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
