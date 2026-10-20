"use client";

import * as React from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { RiskBadge, ContaminationBadge, AnomalyBadge, DepthBadge } from "@/components/ui/badge";
import { MOCK_WELLS, getWells } from "@/data/mock-wells";
import type { RiskLevel, ContaminationStatus, Well } from "@/types";
import {
  Search,
  Filter,
  Download,
  ArrowUpDown,
  ExternalLink,
  ChevronLeft,
  ChevronRight,
  Droplets,
  RotateCcw,
} from "lucide-react";
import { formatNumber } from "@/lib/utils";
import { exportWellsToCSV } from "@/lib/export";

export default function WellsPage() {
  const [search, setSearch] = React.useState("");
  const [selectedState, setSelectedState] = React.useState("all");
  const [selectedRisk, setSelectedRisk] = React.useState<string>("all");
  const [selectedStatus, setSelectedStatus] = React.useState<string>("all");
  const [selectedAnomaly, setSelectedAnomaly] = React.useState<string>("all");
  const [sortBy, setSortBy] = React.useState<keyof Well>("id");
  const [sortOrder, setSortOrder] = React.useState<"asc" | "desc">("asc");

  // Filtering logic
  const filteredWells = React.useMemo(() => {
    return MOCK_WELLS.filter((w) => {
      // Search text
      if (search) {
        const q = search.toLowerCase();
        const match =
          w.station.toLowerCase().includes(q) ||
          w.id.toLowerCase().includes(q) ||
          w.district.toLowerCase().includes(q) ||
          w.state.toLowerCase().includes(q);
        if (!match) return false;
      }
      // State
      if (selectedState !== "all" && w.state.toLowerCase() !== selectedState.toLowerCase()) {
        return false;
      }
      // Risk
      if (selectedRisk !== "all" && w.riskLevel !== selectedRisk) {
        return false;
      }
      // Status
      if (selectedStatus !== "all" && w.status !== selectedStatus) {
        return false;
      }
      // Anomaly
      if (selectedAnomaly === "anomaly" && !w.isAnomaly) return false;
      if (selectedAnomaly === "normal" && w.isAnomaly) return false;

      return true;
    }).sort((a, b) => {
      const valA = a[sortBy];
      const valB = b[sortBy];
      if (valA === null || valA === undefined) return 1;
      if (valB === null || valB === undefined) return -1;
      if (valA < valB) return sortOrder === "asc" ? -1 : 1;
      if (valA > valB) return sortOrder === "asc" ? 1 : -1;
      return 0;
    });
  }, [search, selectedState, selectedRisk, selectedStatus, selectedAnomaly, sortBy, sortOrder]);

  const handleSort = (field: keyof Well) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(field);
      setSortOrder("desc");
    }
  };

  const resetFilters = () => {
    setSearch("");
    setSelectedState("all");
    setSelectedRisk("all");
    setSelectedStatus("all");
    setSelectedAnomaly("all");
  };

  return (
    <AppShell
      title="Groundwater Well Inventory"
      subtitle="Surveillance Exploration, Hydro-Geological Features & Laboratory Records"
    >
      {/* Top Filter & Action Bar */}
      <Card className="p-5 shadow-lg shadow-black/20">
        <div className="flex flex-col gap-3.5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            {/* Search Input */}
            <div className="relative flex-1 min-w-[240px]">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
              <Input
                placeholder="Search station, well ID, district, or state..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-9 h-9"
              />
            </div>

            {/* Quick Actions */}
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={resetFilters} className="text-xs gap-1 border-white/15 text-slate-300 hover:text-white hover:bg-white/5">
                <RotateCcw className="h-3 w-3" />
                <span>Reset</span>
              </Button>
              <Button
                variant="primary"
                size="sm"
                className="text-xs gap-1.5 bg-blue-600 hover:bg-blue-500 text-white shadow-sm shadow-blue-500/20"
                onClick={() => exportWellsToCSV(filteredWells)}
              >
                <Download className="h-3.5 w-3.5" />
                <span>Export CSV ({filteredWells.length})</span>
              </Button>
            </div>
          </div>

          {/* Filter Dropdowns Row */}
          <div className="flex flex-wrap items-center gap-2.5 pt-3 border-t border-white/8 text-xs">
            <span className="text-slate-400 font-medium text-[11px] uppercase tracking-wider mr-1">
              Filters:
            </span>

            {/* State */}
            <Select value={selectedState} onChange={(e) => setSelectedState(e.target.value)}>
              <option value="all">State: All States</option>
              <option value="maharashtra">Maharashtra</option>
              <option value="andhra pradesh">Andhra Pradesh</option>
              <option value="west bengal">West Bengal</option>
              <option value="rajasthan">Rajasthan</option>
              <option value="gujarat">Gujarat</option>
            </Select>

            {/* Risk Tier */}
            <Select value={selectedRisk} onChange={(e) => setSelectedRisk(e.target.value)}>
              <option value="all">Risk: All Tiers</option>
              <option value="critical">Critical Risk</option>
              <option value="high">High Risk</option>
              <option value="medium">Medium Risk</option>
              <option value="low">Low Risk</option>
            </Select>

            {/* Contamination Status */}
            <Select value={selectedStatus} onChange={(e) => setSelectedStatus(e.target.value)}>
              <option value="all">Status: All Records</option>
              <option value="contaminated">Contaminated (EC &gt; 3000)</option>
              <option value="clean">Clean (Potable)</option>
              <option value="untested">Untested</option>
            </Select>

            {/* Anomaly Flag */}
            <Select value={selectedAnomaly} onChange={(e) => setSelectedAnomaly(e.target.value)}>
              <option value="all">Anomalies: All Wells</option>
              <option value="anomaly">Flagged Anomaly Only</option>
              <option value="normal">Normal Only</option>
            </Select>

            <span className="ml-auto text-slate-400 font-mono text-[11px]">
              Showing {filteredWells.length} of {MOCK_WELLS.length} monitored sample wells
            </span>
          </div>
        </div>
      </Card>

      {/* Main Table */}
      <Card className="overflow-hidden shadow-lg shadow-black/20">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead onClick={() => handleSort("id")} className="cursor-pointer hover:text-white w-28">
                <div className="flex items-center gap-1">
                  <span>Well ID</span>
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </TableHead>
              <TableHead onClick={() => handleSort("station")} className="cursor-pointer hover:text-white">
                <div className="flex items-center gap-1">
                  <span>Station / District</span>
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </TableHead>
              <TableHead>State</TableHead>
              <TableHead onClick={() => handleSort("groundwaterLevelM")} className="text-right cursor-pointer hover:text-white">
                <div className="flex items-center justify-end gap-1">
                  <span>Depth (GWL)</span>
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </TableHead>
              <TableHead onClick={() => handleSort("ecValue")} className="text-right cursor-pointer hover:text-white">
                <div className="flex items-center justify-end gap-1">
                  <span>Conductivity (EC)</span>
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </TableHead>
              <TableHead onClick={() => handleSort("contaminationProbability")} className="text-right cursor-pointer hover:text-white">
                <div className="flex items-center justify-end gap-1">
                  <span>ML Risk Prob</span>
                  <ArrowUpDown className="h-3 w-3" />
                </div>
              </TableHead>
              <TableHead>Cluster</TableHead>
              <TableHead>Anomaly Flag</TableHead>
              <TableHead className="text-right">Action</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredWells.length === 0 ? (
              <TableRow>
                <TableCell colSpan={9} className="text-center py-10 text-slate-400">
                  No wells match the selected filter criteria.
                </TableCell>
              </TableRow>
            ) : (
              filteredWells.map((well) => (
                <TableRow key={well.id} className="hover:bg-white/[0.03] transition-colors">
                  {/* Well ID */}
                  <TableCell className="font-mono font-semibold text-xs">
                    <Link
                      href={`/wells/${well.id}`}
                      className="text-blue-400 hover:text-blue-300 hover:underline transition-colors"
                    >
                      {well.id}
                    </Link>
                  </TableCell>

                  {/* Station & District */}
                  <TableCell>
                    <div className="flex flex-col">
                      <span className="font-semibold text-white text-xs">
                        {well.station}
                      </span>
                      <span className="text-[11px] text-slate-400 capitalize">
                        {well.district}
                      </span>
                    </div>
                  </TableCell>

                  {/* State */}
                  <TableCell className="capitalize text-slate-300 text-xs font-medium">
                    {well.state}
                  </TableCell>

                  {/* Depth */}
                  <TableCell className="text-right">
                    <DepthBadge
                      category={well.gwDepthCategory}
                      depthM={well.groundwaterLevelM}
                    />
                  </TableCell>

                  {/* EC Value */}
                  <TableCell className="text-right font-mono text-xs font-semibold">
                    {well.ecValue ? (
                      <span
                        className={
                          well.ecValue > 3000
                            ? "text-rose-300 bg-rose-500/15 px-2 py-0.5 rounded-full border border-rose-500/30"
                            : "text-slate-200"
                        }
                      >
                        {formatNumber(well.ecValue)} µS/cm
                      </span>
                    ) : (
                      <span className="text-slate-400">Untested</span>
                    )}
                  </TableCell>

                  {/* Contamination Probability & Risk Badge */}
                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-2">
                      <span className="font-mono text-xs font-semibold text-slate-200">
                        {well.contaminationProbability
                          ? `${(well.contaminationProbability * 100).toFixed(0)}%`
                          : "N/A"}
                      </span>
                      <RiskBadge level={well.riskLevel} />
                    </div>
                  </TableCell>

                  {/* Cluster DBSCAN */}
                  <TableCell>
                    <span className="rounded-full bg-white/5 px-2 py-0.5 text-[11px] font-mono text-slate-300 border border-white/10">
                      #{well.clusterDbscan}
                    </span>
                  </TableCell>

                  {/* Anomaly Badge */}
                  <TableCell>
                    {well.isAnomaly ? (
                      <AnomalyBadge isAnomaly={true} score={well.anomalyScore} />
                    ) : (
                      <span className="text-[11px] text-slate-400 font-mono">Normal</span>
                    )}
                  </TableCell>

                  {/* Inspect Details Link */}
                  <TableCell className="text-right">
                    <Link href={`/wells/${well.id}`}>
                      <Button variant="outline" size="xs" className="h-7 text-[11px] gap-1.5 border-white/15 text-slate-200 hover:text-white hover:bg-white/5">
                        <span>Details</span>
                        <ExternalLink className="h-3 w-3" />
                      </Button>
                    </Link>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </Card>
    </AppShell>
  );
}
