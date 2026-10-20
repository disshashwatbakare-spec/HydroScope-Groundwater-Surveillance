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
import { RiskBadge, AnomalyBadge } from "@/components/ui/badge";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import {
  Sparkles,
  ExternalLink,
  CheckCircle2,
  Send,
  ArrowRight,
} from "lucide-react";
import { MOCK_TESTING_QUEUE } from "@/data/mock-wells";

export function PriorityWells() {
  const [allocatedIds, setAllocatedIds] = React.useState<string[]>([
    "MH-NSK-002",
  ]);

  const toggleAllocate = (id: string) => {
    setAllocatedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  return (
    <Card className="h-full flex flex-col shadow-lg shadow-black/20">
      <CardHeader className="p-5 pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <CardTitle className="text-sm font-semibold text-white tracking-tight">
              Priority Field Testing Queue
            </CardTitle>
            <span className="rounded-full bg-blue-500/10 px-2.5 py-0.5 text-[10px] font-semibold text-blue-300 border border-blue-500/30">
              Top Recommendations
            </span>
          </div>
          <Link href="/testing-queue">
            <Button variant="ghost" size="xs" className="h-7 text-xs text-blue-400 gap-1 hover:text-blue-300 hover:bg-white/5">
              <span>Full Queue</span>
              <ArrowRight className="h-3 w-3" />
            </Button>
          </Link>
        </div>
        <CardDescription className="text-xs text-slate-400">
          Wells prioritized by risk uncertainty and local anomaly flags for this month&apos;s testing allocation
        </CardDescription>
      </CardHeader>

      <CardContent className="p-0 flex-1">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-12 text-center text-xs">Rank</TableHead>
              <TableHead className="text-xs">Station & District</TableHead>
              <TableHead className="text-xs">Risk Tier</TableHead>
              <TableHead className="text-xs">Why Prioritized?</TableHead>
              <TableHead className="text-right text-xs">Action</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {MOCK_TESTING_QUEUE.map((item) => {
              const isAllocated = allocatedIds.includes(item.well.id);

              return (
                <TableRow key={item.well.id} className="hover:bg-white/[0.03]">
                  {/* Rank */}
                  <TableCell className="text-center font-mono font-bold text-xs text-blue-400">
                    #{item.rank}
                  </TableCell>

                  {/* Station & Location */}
                  <TableCell>
                    <div className="flex flex-col">
                      <Link
                        href={`/wells/${item.well.id}`}
                        className="font-semibold text-xs text-white hover:text-blue-400 hover:underline transition-colors"
                      >
                        {item.well.station}
                      </Link>
                      <span className="text-[11px] text-slate-400 capitalize">
                        {item.well.district}, {item.well.state}
                      </span>
                    </div>
                  </TableCell>

                  {/* Risk Badge */}
                  <TableCell>
                    <RiskBadge level={item.well.riskLevel} />
                  </TableCell>

                  {/* Plain English Reason Drivers */}
                  <TableCell>
                    <div className="flex flex-wrap gap-1">
                      {item.well.isAnomaly && (
                        <span className="rounded-md bg-violet-500/15 px-1.5 py-0.5 text-[10px] font-medium text-violet-300 border border-violet-500/30">
                          Outlier Reading
                        </span>
                      )}
                      {item.well.groundwaterLevelM && item.well.groundwaterLevelM < 5 && (
                        <span className="rounded-md bg-cyan-500/15 px-1.5 py-0.5 text-[10px] font-medium text-cyan-300 border border-cyan-500/30">
                          Shallow Water Table
                        </span>
                      )}
                      {item.well.bbnClusterRisk === 1 && (
                        <span className="rounded-md bg-amber-500/15 px-1.5 py-0.5 text-[10px] font-medium text-amber-300 border border-amber-500/30">
                          Nearby Salinity
                        </span>
                      )}
                    </div>
                  </TableCell>

                  {/* Action Button */}
                  <TableCell className="text-right">
                    <Button
                      variant={isAllocated ? "secondary" : "primary"}
                      size="xs"
                      onClick={() => toggleAllocate(item.well.id)}
                      className={`gap-1 h-7 text-xs ${
                        isAllocated
                          ? "bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/25"
                          : "bg-blue-600 hover:bg-blue-500 text-white shadow-xs shadow-blue-500/20"
                      }`}
                    >
                      {isAllocated ? (
                        <>
                          <CheckCircle2 className="h-3 w-3" />
                          <span>Kit Sent</span>
                        </>
                      ) : (
                        <>
                          <Send className="h-3 w-3" />
                          <span>Dispatch Kit</span>
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
  );
}
