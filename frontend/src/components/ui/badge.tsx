import * as React from "react";
import { cn } from "@/lib/utils";
import type { RiskLevel, ContaminationStatus, WellDepthCategory } from "@/types";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "secondary" | "outline" | "danger" | "warning" | "success" | "muted";
}

export function Badge({
  className,
  variant = "default",
  ...props
}: BadgeProps) {
  const variantStyles = {
    default: "bg-blue-600/20 text-blue-300 border-blue-500/30",
    secondary: "bg-white/5 text-slate-300 border-white/10",
    outline: "border border-white/15 text-slate-300 bg-transparent",
    danger: "bg-rose-500/15 text-rose-300 border-rose-500/30",
    warning: "bg-amber-500/15 text-amber-300 border-amber-500/30",
    success: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
    muted: "bg-white/5 text-slate-400 border-white/10",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium border tracking-tight",
        variantStyles[variant],
        className
      )}
      {...props}
    />
  );
}

export function RiskBadge({ level }: { level: RiskLevel }) {
  const styles: Record<RiskLevel, { label: string; cls: string; dot: string }> = {
    critical: {
      label: "Critical Risk",
      cls: "bg-rose-500/15 text-rose-300 border-rose-500/30",
      dot: "bg-rose-400",
    },
    high: {
      label: "High Risk",
      cls: "bg-amber-500/15 text-amber-300 border-amber-500/30",
      dot: "bg-amber-400",
    },
    medium: {
      label: "Medium Risk",
      cls: "bg-blue-500/15 text-blue-300 border-blue-500/30",
      dot: "bg-blue-400",
    },
    low: {
      label: "Low Risk",
      cls: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
      dot: "bg-emerald-400",
    },
  };

  const item = styles[level] || styles.low;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[11px] font-medium border backdrop-blur-xs",
        item.cls
      )}
    >
      <span className={cn("h-1.5 w-1.5 rounded-full shrink-0", item.dot)} />
      {item.label}
    </span>
  );
}

export function ContaminationBadge({ status }: { status: ContaminationStatus }) {
  if (status === "contaminated") {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-rose-500/15 px-2.5 py-0.5 text-[11px] font-medium text-rose-300 border border-rose-500/30">
        <span className="h-1.5 w-1.5 rounded-full bg-rose-400 shrink-0" />
        Contaminated
      </span>
    );
  }
  if (status === "clean") {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-[11px] font-medium text-emerald-300 border border-emerald-500/30">
        <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shrink-0" />
        Clean (Potable)
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5 rounded-full bg-white/5 px-2.5 py-0.5 text-[11px] font-medium text-slate-400 border border-white/10">
      <span className="h-1.5 w-1.5 rounded-full bg-slate-500 shrink-0" />
      Untested (Prioritized)
    </span>
  );
}

export function AnomalyBadge({ isAnomaly, score }: { isAnomaly: boolean; score?: number | null }) {
  if (!isAnomaly) return null;
  return (
    <span className="inline-flex items-center gap-1.5 rounded-full bg-violet-500/15 px-2.5 py-0.5 text-[11px] font-medium text-violet-300 border border-violet-500/30">
      <span className="h-1.5 w-1.5 rounded-full bg-violet-400 shrink-0" />
      Cluster Anomaly
      {score !== undefined && score !== null && (
        <span className="font-mono opacity-80">({score.toFixed(2)})</span>
      )}
    </span>
  );
}

export function DepthBadge({ category, depthM }: { category: WellDepthCategory; depthM?: number | null }) {
  const labels: Record<WellDepthCategory, string> = {
    shallow: "Shallow (<5m)",
    medium: "Mid-depth (5-15m)",
    deep: "Deep (>15m)",
  };

  return (
    <span className="inline-flex items-center gap-1.5 rounded-full bg-white/5 px-2.5 py-0.5 text-[11px] font-medium text-slate-300 border border-white/10">
      <span>{labels[category] || category}</span>
      {depthM !== undefined && depthM !== null && (
        <span className="text-slate-400 font-mono">({depthM.toFixed(1)}m)</span>
      )}
    </span>
  );
}
