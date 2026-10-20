"use client";

import * as React from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { formatNumber } from "@/lib/utils";
import { MOCK_RISK_DISTRIBUTION } from "@/data/mock-wells";

export function RiskDistribution() {
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const total = MOCK_RISK_DISTRIBUTION.reduce((acc, curr) => acc + curr.count, 0);

  return (
    <Card className="h-full flex flex-col shadow-lg shadow-black/20">
      <CardHeader className="p-5 pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-semibold text-white tracking-tight">Contamination Risk Distribution</CardTitle>
          <span className="text-[11px] font-mono text-slate-300 bg-white/5 border border-white/10 px-2.5 py-0.5 rounded-full">
            N = {formatNumber(total)} Wells
          </span>
        </div>
        <CardDescription className="text-xs text-slate-400">
          Multi-state population classified via calibrated Random Forest + SMOTE
        </CardDescription>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col justify-between pt-0 pb-4">
        {/* Chart View */}
        <div className="h-44 w-full relative flex items-center justify-center my-1">
          {mounted ? (
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={MOCK_RISK_DISTRIBUTION}
                  cx="50%"
                  cy="50%"
                  innerRadius={48}
                  outerRadius={72}
                  paddingAngle={2}
                  dataKey="count"
                >
                  {MOCK_RISK_DISTRIBUTION.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="#0D1526" strokeWidth={2} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value: any, name: any) => [
                    `${formatNumber(Number(value))} wells (${((Number(value) / total) * 100).toFixed(1)}%)`,
                    name,
                  ]}
                  contentStyle={{
                    backgroundColor: "#0D1526",
                    borderColor: "rgba(255,255,255,0.15)",
                    borderRadius: "12px",
                    fontSize: "12px",
                    color: "#ffffff",
                    boxShadow: "0 8px 16px rgba(0,0,0,0.4)",
                  }}
                  itemStyle={{ color: "#ffffff" }}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-slate-400">
              Loading distribution...
            </div>
          )}

          {/* Centered Donut Summary */}
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span className="text-lg font-bold text-white font-mono">
              5.6%
            </span>
            <span className="text-[10px] text-slate-400 font-medium">
              High / Critical
            </span>
          </div>
        </div>

        {/* Legend Breakdown List */}
        <div className="space-y-2 border-t border-white/5 pt-3">
          {MOCK_RISK_DISTRIBUTION.map((item, idx) => (
            <div key={idx} className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <span
                  className="h-2.5 w-2.5 rounded-full shrink-0 shadow-xs"
                  style={{ backgroundColor: item.color }}
                />
                <span className="text-slate-300 font-medium text-[11px] truncate">
                  {item.name}
                </span>
              </div>
              <div className="flex items-center gap-2 font-mono text-[11px]">
                <span className="text-white font-semibold">
                  {formatNumber(item.count)}
                </span>
                <span className="text-slate-400 w-12 text-right">
                  {item.percentage}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
