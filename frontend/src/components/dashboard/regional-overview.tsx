"use client";

import * as React from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { formatNumber, formatPct } from "@/lib/utils";
import { MOCK_REGIONAL_STATS, type RegionalStat } from "@/data/mock-wells";
import { MapPin, TrendingUp, AlertCircle } from "lucide-react";

export function RegionalOverview() {
  return (
    <Card className="h-full flex flex-col shadow-lg shadow-black/20">
      <CardHeader className="p-5 pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-semibold text-white tracking-tight">Regional Contamination & Hydrology Overview</CardTitle>
          <span className="text-[11px] font-mono text-slate-300 bg-white/5 border border-white/10 px-2.5 py-0.5 rounded-full">
            5 State Zones
          </span>
        </div>
        <CardDescription className="text-xs text-slate-400">
          Comparison of groundwater salinity (EC), depth to water table (GWL), and cluster anomaly density
        </CardDescription>
      </CardHeader>

      <CardContent className="p-0 flex-1">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[180px]">State Zone</TableHead>
              <TableHead className="text-right">Monitored Wells</TableHead>
              <TableHead className="text-right">Contamination Rate</TableHead>
              <TableHead className="text-right">Anomalies</TableHead>
              <TableHead className="text-right">Avg GWL (Depth)</TableHead>
              <TableHead className="text-right">Avg EC (Salinity)</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {MOCK_REGIONAL_STATS.map((reg) => {
              const isHighSaline = reg.avgEc > 3000;
              const isDeep = reg.avgGwl > 20;

              return (
                <TableRow key={reg.stateCode} className="hover:bg-white/[0.03]">
                  <TableCell className="font-medium text-white">
                    <div className="flex items-center gap-2.5">
                      <span className="h-2 w-2 rounded-full bg-blue-400 shrink-0" />
                      <div>
                        <div className="font-semibold text-xs text-white">
                          {reg.state}
                        </div>
                        <div className="text-[10px] text-slate-400 font-mono">
                          Zone code: {reg.stateCode}
                        </div>
                      </div>
                    </div>
                  </TableCell>

                  <TableCell className="text-right font-mono text-xs font-medium text-slate-200">
                    {formatNumber(reg.totalWells)}
                  </TableCell>

                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-2">
                      <div className="w-16 bg-white/10 h-1.5 rounded-full overflow-hidden hidden sm:block">
                        <div
                          className={`h-full rounded-full ${
                            reg.contaminationRate > 0.1
                              ? "bg-rose-500"
                              : reg.contaminationRate > 0.05
                              ? "bg-amber-500"
                              : "bg-emerald-500"
                          }`}
                          style={{
                            width: `${Math.min(reg.contaminationRate * 600, 100)}%`,
                          }}
                        />
                      </div>
                      <span
                        className={`font-mono text-xs font-semibold ${
                          reg.contaminationRate > 0.1
                            ? "text-rose-400"
                            : reg.contaminationRate > 0.05
                            ? "text-amber-400"
                            : "text-emerald-400"
                        }`}
                      >
                        {formatPct(reg.contaminationRate)}
                      </span>
                    </div>
                  </TableCell>

                  <TableCell className="text-right font-mono text-xs text-violet-400 font-medium">
                    {formatNumber(reg.anomalies)}
                  </TableCell>

                  <TableCell className="text-right font-mono text-xs text-slate-200">
                    <span className={isDeep ? "font-semibold text-amber-300" : ""}>
                      {reg.avgGwl.toFixed(1)} m
                    </span>
                  </TableCell>

                  <TableCell className="text-right font-mono text-xs">
                    <span
                      className={`px-2 py-0.5 rounded-full text-[11px] ${
                        isHighSaline
                          ? "bg-rose-500/15 text-rose-300 font-semibold border border-rose-500/30"
                          : "text-slate-200"
                      }`}
                    >
                      {formatNumber(reg.avgEc)} µS/cm
                    </span>
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
