"use client";

import * as React from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { RiskBadge, AnomalyBadge, DepthBadge } from "@/components/ui/badge";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { MOCK_TESTING_QUEUE, MOCK_WELLS } from "@/data/mock-wells";
import {
  Sparkles,
  Send,
  CheckCircle2,
  Calendar,
  AlertTriangle,
  Layers,
  ArrowRight,
  TrendingUp,
  Download,
  Info,
  Check,
} from "lucide-react";
import { formatNumber } from "@/lib/utils";
import { exportQueueToCSV } from "@/lib/export";

export default function TestingQueuePage() {
  const [allocatedIds, setAllocatedIds] = React.useState<string[]>([
    "MH-NSK-002",
    "MH-LTR-004",
  ]);
  const [budgetLimit, setBudgetLimit] = React.useState(50);
  const [strategy, setStrategy] = React.useState("uncertainty_bbn");

  const toggleAllocate = (id: string) => {
    setAllocatedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const allocateAllTop = () => {
    setAllocatedIds(MOCK_TESTING_QUEUE.map((q) => q.well.id));
  };

  return (
    <AppShell
      title="Active-Learning Testing Priority Queue"
      subtitle="Surveillance Resource-Allocation & Epistemic Uncertainty Sampling"
    >
      {/* Top Budget Management & Strategy Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Budget Status */}
        <Card className="p-5 shadow-lg shadow-black/20">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
            <span className="font-semibold uppercase tracking-wider text-[10px]">
              Monthly Testing Budget
            </span>
            <Sparkles className="h-4 w-4 text-blue-400" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold font-mono text-white">
              {allocatedIds.length}
            </span>
            <span className="text-xs font-mono text-slate-400">
              / {budgetLimit} Wells Allocated
            </span>
          </div>
          {/* Progress Bar */}
          <div className="mt-3.5 w-full bg-white/10 h-2 rounded-full overflow-hidden">
            <div
              className="bg-blue-500 h-full rounded-full transition-all duration-300 shadow-xs shadow-blue-500/50"
              style={{ width: `${(allocatedIds.length / budgetLimit) * 100}%` }}
            />
          </div>
          <div className="mt-2.5 text-[10px] text-slate-400 flex justify-between">
            <span>{budgetLimit - allocatedIds.length} Tests remaining</span>
            <span>Capacity: 50/mo</span>
          </div>
        </Card>

        {/* Discovery Efficiency Callout */}
        <Card className="p-5 shadow-lg shadow-black/20">
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
            <span className="font-semibold uppercase tracking-wider text-[10px]">
              Active vs Random Sampling
            </span>
            <TrendingUp className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold font-mono text-emerald-400">
              +86.4%
            </span>
            <span className="text-xs text-slate-400">
              Contamination Detection Gain
            </span>
          </div>
          <p className="mt-2.5 text-[11px] text-slate-400 leading-relaxed">
            Uncertainty sampling uncovers 2.1x more contaminated wells within the same laboratory budget compared to uniform random sampling.
          </p>
        </Card>

        {/* Dispatch Controls */}
        <Card className="p-5 shadow-lg shadow-black/20 flex flex-col justify-between">
          <div>
            <div className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Field Strategy
            </div>
            <Select
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
              className="w-full text-xs"
            >
              <option value="uncertainty_bbn">Uncertainty + Bayesian BBN (Recommended)</option>
              <option value="entropy_pure">Pure Epistemic Entropy</option>
              <option value="anomaly_first">Anomaly Outliers First (Isolation Forest)</option>
              <option value="shallow_vulnerable">Shallow Aquifer Risk First</option>
            </Select>
          </div>
          <div className="mt-4 flex items-center gap-2">
            <Button
              variant="primary"
              size="sm"
              onClick={allocateAllTop}
              className="w-full text-xs gap-1.5 bg-blue-600 hover:bg-blue-500 text-white shadow-sm shadow-blue-500/20"
            >
              <Check className="h-3.5 w-3.5" />
              <span>Allocate All Top 5</span>
            </Button>
          </div>
        </Card>
      </div>

      {/* Main Priority Queue Table */}
      <Card className="shadow-lg shadow-black/20 overflow-hidden">
        <CardHeader className="border-b border-white/8 p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <CardTitle className="text-sm font-semibold text-white tracking-tight">Prioritized Wells for Immediate Lab Verification</CardTitle>
              <CardDescription className="text-xs text-slate-400">
                Ranked by model decision margin, cluster risk, and within-cluster anomaly scores
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="primary"
                size="sm"
                className="text-xs gap-1.5 bg-blue-600 hover:bg-blue-500 text-white shadow-sm shadow-blue-500/20"
                onClick={() => exportQueueToCSV(MOCK_TESTING_QUEUE)}
              >
                <Download className="h-3.5 w-3.5" />
                <span>Export Field Dispatch CSV</span>
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-14 text-center">Rank</TableHead>
                <TableHead>Monitoring Station & Location</TableHead>
                <TableHead>Risk Classification</TableHead>
                <TableHead className="text-right">Uncertainty Score</TableHead>
                <TableHead className="text-right">BBN Contamination Prob</TableHead>
                <TableHead>Causal Decision Factors</TableHead>
                <TableHead>Last Field Record</TableHead>
                <TableHead className="text-right">Lab Dispatch Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {MOCK_TESTING_QUEUE.map((item) => {
                const isAllocated = allocatedIds.includes(item.well.id);

                return (
                  <TableRow key={item.well.id} className="hover:bg-white/[0.03]">
                    {/* Rank */}
                    <TableCell className="text-center font-mono font-bold text-sm text-blue-400">
                      #{item.rank}
                    </TableCell>

                    {/* Station & Location */}
                    <TableCell>
                      <div className="flex flex-col">
                        <div className="flex items-center gap-1.5 font-semibold text-xs text-white">
                          <Link
                            href={`/wells/${item.well.id}`}
                            className="hover:underline hover:text-blue-400 transition-colors"
                          >
                            {item.well.station}
                          </Link>
                          <span className="font-mono text-[10px] text-slate-400 bg-white/5 border border-white/10 px-1.5 py-0.5 rounded-full">
                            {item.well.id}
                          </span>
                        </div>
                        <div className="text-[11px] text-slate-400 capitalize mt-0.5">
                          {item.well.district}, {item.well.state} • Cluster #{item.well.clusterDbscan}
                        </div>
                      </div>
                    </TableCell>

                    {/* Risk Badge */}
                    <TableCell>
                      <RiskBadge level={item.well.riskLevel} />
                    </TableCell>

                    {/* Uncertainty Score */}
                    <TableCell className="text-right font-mono text-xs">
                      <span className="font-semibold text-blue-300 bg-blue-500/15 px-2.5 py-0.5 rounded-full border border-blue-500/30">
                        {item.uncertaintyScore.toFixed(2)}
                      </span>
                    </TableCell>

                    {/* BBN Posterior Probability & ML Risk */}
                    <TableCell className="text-right font-mono text-xs">
                      <div className="font-bold text-white">
                        {(item.bbnContaminationProbability * 100).toFixed(0)}%
                      </div>
                      <div className="text-[10px] text-slate-400">
                        ML: {((item.well.contaminationProbability || 0) * 100).toFixed(0)}%
                      </div>
                    </TableCell>

                    {/* Causal Flags */}
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {item.well.isAnomaly && (
                          <span className="rounded-md bg-violet-500/15 px-2 py-0.5 text-[10px] font-medium text-violet-300 border border-violet-500/30">
                            Anomaly ({item.well.anomalyScore?.toFixed(2)})
                          </span>
                        )}
                        {item.well.groundwaterLevelM && item.well.groundwaterLevelM < 5 && (
                          <span className="rounded-md bg-cyan-500/15 px-2 py-0.5 text-[10px] font-medium text-cyan-300 border border-cyan-500/30">
                            Shallow Infiltration
                          </span>
                        )}
                        {item.well.bbnClusterRisk === 1 && (
                          <span className="rounded-md bg-amber-500/15 px-2 py-0.5 text-[10px] font-medium text-amber-300 border border-amber-500/30">
                            Saline Cluster
                          </span>
                        )}
                        {item.well.bbnDistrictUrban === 1 && (
                          <span className="rounded-md bg-white/5 px-2 py-0.5 text-[10px] font-medium text-slate-300 border border-white/10">
                            Urban District
                          </span>
                        )}
                      </div>
                    </TableCell>

                    {/* Last Tested */}
                    <TableCell className="text-xs text-slate-400 font-mono">
                      {item.well.lastTestedDate}
                    </TableCell>

                    {/* Dispatch Action */}
                    <TableCell className="text-right">
                      <Button
                        variant={isAllocated ? "secondary" : "primary"}
                        size="xs"
                        onClick={() => toggleAllocate(item.well.id)}
                        className={`gap-1.5 h-7 text-xs ${
                          isAllocated
                            ? "bg-emerald-500/15 text-emerald-300 border-emerald-500/30 hover:bg-emerald-500/25"
                            : "bg-blue-600 hover:bg-blue-500 text-white shadow-xs shadow-blue-500/20"
                        }`}
                      >
                        {isAllocated ? (
                          <>
                            <CheckCircle2 className="h-3 w-3" />
                            <span>Kit Allocated</span>
                          </>
                        ) : (
                          <>
                            <Send className="h-3 w-3" />
                            <span>Allocate Test</span>
                          </>
                        )}
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </AppShell>
  );
}
