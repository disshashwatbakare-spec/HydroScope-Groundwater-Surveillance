"use client";

import * as React from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Layers,
  MapPin,
  Droplets,
  ListOrdered,
} from "lucide-react";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  title?: string;
  subtitle?: string;
}

const STATE_OPTIONS = [
  { value: "all", label: "All 5 States" },
  { value: "maharashtra", label: "Maharashtra" },
  { value: "andhra pradesh", label: "Andhra Pradesh" },
  { value: "west bengal", label: "West Bengal" },
  { value: "rajasthan", label: "Rajasthan" },
  { value: "gujarat", label: "Gujarat" },
];

export function Header({
  title = "Surveillance Dashboard",
  subtitle = "Groundwater Quality Monitoring & Active-Learning Resource Allocation",
}: HeaderProps) {
  const router = useRouter();
  const [selectedState, setSelectedState] = React.useState("all");

  const handleStateChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setSelectedState(val);
    // Navigate to the Map page pre-filtered by state
    if (val === "all") {
      router.push("/map");
    } else {
      router.push(`/map?state=${encodeURIComponent(val)}`);
    }
  };

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-white/8 bg-[#080E1A]/90 px-6 backdrop-blur-xl">
      <div className="flex flex-col">
        <h1 className="text-sm font-semibold text-white tracking-tight">
          {title}
        </h1>
        <p className="text-xs text-slate-400 font-normal">
          {subtitle}
        </p>
      </div>

      <div className="flex items-center gap-3">
        {/* Quick Jump Buttons to the 3 core features */}
        <div className="hidden lg:flex items-center gap-1.5 border-r border-white/10 pr-3">
          <Link href="/map">
            <Button variant="ghost" size="xs" className="h-7 text-xs text-slate-300 gap-1.5 hover:text-white hover:bg-white/5">
              <MapPin className="h-3.5 w-3.5 text-blue-400" />
              <span>Map</span>
            </Button>
          </Link>
          <Link href="/wells">
            <Button variant="ghost" size="xs" className="h-7 text-xs text-slate-300 gap-1.5 hover:text-white hover:bg-white/5">
              <Droplets className="h-3.5 w-3.5 text-cyan-400" />
              <span>Wells</span>
            </Button>
          </Link>
          <Link href="/testing-queue">
            <Button variant="ghost" size="xs" className="h-7 text-xs text-slate-300 gap-1.5 hover:text-white hover:bg-white/5">
              <ListOrdered className="h-3.5 w-3.5 text-indigo-400" />
              <span>Queue</span>
            </Button>
          </Link>
        </div>

        {/* Region / State Filter */}
        <div
          className={`flex items-center gap-1.5 rounded-xl border px-3 py-1.5 text-xs transition-all ${
            selectedState !== "all"
              ? "border-blue-500/50 bg-blue-500/15 text-blue-200 shadow-xs shadow-blue-500/10"
              : "border-white/10 bg-[#0D1526]/80 text-slate-300 hover:border-white/20"
          }`}
        >
          <Layers
            className={`h-3.5 w-3.5 ${
              selectedState !== "all" ? "text-blue-400" : "text-slate-400"
            }`}
          />
          <span
            className={`text-[11px] font-medium ${
              selectedState !== "all" ? "text-blue-300" : "text-slate-400"
            }`}
          >
            Region:
          </span>
          <select
            value={selectedState}
            onChange={handleStateChange}
            className="bg-transparent text-xs font-semibold focus:outline-none cursor-pointer text-white [&>option]:bg-[#080E1A] [&>option]:text-slate-200"
          >
            {STATE_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        {/* Testing Budget Pill */}
        <div className="hidden sm:flex items-center gap-2 rounded-xl border border-blue-500/30 bg-blue-500/10 px-3 py-1.5 text-xs text-blue-200 font-medium">
          <span className="h-2 w-2 rounded-full bg-blue-400 animate-pulse shrink-0" />
          <span className="text-[11px] text-blue-300">Lab Budget:</span>
          <span className="font-mono font-semibold text-white">50 / Month</span>
        </div>
      </div>
    </header>
  );
}
