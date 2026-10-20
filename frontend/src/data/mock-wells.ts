import type {
  Well,
  RiskLevel,
  WellDepthCategory,
  DashboardKPIs,
  TestingQueueEntry,
  TestingReason,
  WellFilter,
} from "@/types";
import { ecToRiskLevel, gwlToDepthCategory } from "@/lib/utils";
import livePipelineData from "./live_pipeline_data.json";

// ─── Real CGWB Seeded Wells ──────────────────────────────────────────────────
// Reflects actual locations from CGWB groundwater records (1961-2025)
const RAW_WELLS = [
  {
    id: "MH-PUN-001",
    station: "Pune Cantonment",
    state: "maharashtra",
    district: "pune",
    lat: 18.5204,
    lon: 73.8567,
    gwl: 8.4,
    ec: 980,
    prob: 0.04,
    anomScore: 0.22,
    isAnom: false,
    clDbscan: 5,
    clAgg: 3,
    clRisk: 0,
    distUrban: 1,
    lastTested: "2024-06-10",
    priority: null,
  },
  {
    id: "MH-NSK-002",
    station: "Nashik Road Industrial",
    state: "maharashtra",
    district: "nashik",
    lat: 19.9975,
    lon: 73.7898,
    gwl: 12.6,
    ec: 3820,
    prob: 0.76,
    anomScore: -0.15,
    isAnom: true,
    clDbscan: 5,
    clAgg: 3,
    clRisk: 1,
    distUrban: 1,
    lastTested: "2023-08-05",
    priority: 1,
  },
  {
    id: "MH-LTR-004",
    station: "Latur Central Deep",
    state: "maharashtra",
    district: "latur",
    lat: 18.4088,
    lon: 76.5604,
    gwl: 6.8,
    ec: 5120,
    prob: 0.92,
    anomScore: -0.28,
    isAnom: true,
    clDbscan: 7,
    clAgg: 5,
    clRisk: 1,
    distUrban: 0,
    lastTested: "2022-12-20",
    priority: 2,
  },
  {
    id: "MH-AMR-003",
    station: "Amravati South Peri",
    state: "maharashtra",
    district: "amravati",
    lat: 20.932,
    lon: 77.7523,
    gwl: 18.2,
    ec: 1750,
    prob: 0.22,
    anomScore: 0.03,
    isAnom: false,
    clDbscan: 6,
    clAgg: 4,
    clRisk: 0,
    distUrban: 0,
    lastTested: "2024-01-15",
    priority: null,
  },
  {
    id: "MH-AUR-005",
    station: "Chhatrapati Sambhajinagar East",
    state: "maharashtra",
    district: "aurangabad",
    lat: 19.8762,
    lon: 75.3433,
    gwl: 11.2,
    ec: 2420,
    prob: 0.38,
    anomScore: 0.02,
    isAnom: false,
    clDbscan: 6,
    clAgg: 4,
    clRisk: 0,
    distUrban: 1,
    lastTested: "2024-03-30",
    priority: 11,
  },
  {
    id: "AP-KRI-001",
    station: "A Konduru Rural Community",
    state: "andhra pradesh",
    district: "krishna",
    lat: 16.965,
    lon: 80.652,
    gwl: 1.8,
    ec: 1539,
    prob: 0.08,
    anomScore: 0.12,
    isAnom: false,
    clDbscan: 2,
    clAgg: 1,
    clRisk: 0,
    distUrban: 0,
    lastTested: "2024-05-01",
    priority: null,
  },
  {
    id: "AP-WGD-002",
    station: "Eluru Canal Basin",
    state: "andhra pradesh",
    district: "west godavari",
    lat: 16.7107,
    lon: 81.0952,
    gwl: 2.3,
    ec: 4260,
    prob: 0.84,
    anomScore: -0.08,
    isAnom: true,
    clDbscan: 2,
    clAgg: 1,
    clRisk: 1,
    distUrban: 1,
    lastTested: "2023-11-15",
    priority: 3,
  },
  {
    id: "AP-GNT-003",
    station: "Narasaraopet Agro Block",
    state: "andhra pradesh",
    district: "guntur",
    lat: 16.2361,
    lon: 80.0499,
    gwl: 5.1,
    ec: 2150,
    prob: 0.31,
    anomScore: 0.05,
    isAnom: false,
    clDbscan: 3,
    clAgg: 2,
    clRisk: 0,
    distUrban: 0,
    lastTested: "2024-02-20",
    priority: null,
  },
  {
    id: "AP-KRN-004",
    station: "Kurnool Tungabhadra Basin",
    state: "andhra pradesh",
    district: "kurnool",
    lat: 15.8281,
    lon: 78.0373,
    gwl: 9.1,
    ec: 3280,
    prob: 0.67,
    anomScore: -0.1,
    isAnom: false,
    clDbscan: 3,
    clAgg: 2,
    clRisk: 1,
    distUrban: 0,
    lastTested: "2024-01-20",
    priority: 10,
  },
  {
    id: "RJ-JOD-001",
    station: "Jodhpur Desert Rim North",
    state: "rajasthan",
    district: "jodhpur",
    lat: 26.2389,
    lon: 73.0243,
    gwl: 35.4,
    ec: 6850,
    prob: 0.95,
    anomScore: -0.41,
    isAnom: true,
    clDbscan: 1,
    clAgg: 0,
    clRisk: 1,
    distUrban: 1,
    lastTested: "2023-05-18",
    priority: 5,
  },
  {
    id: "RJ-BIK-002",
    station: "Bikaner Saline Belt Station",
    state: "rajasthan",
    district: "bikaner",
    lat: 28.0229,
    lon: 73.3119,
    gwl: 42.1,
    ec: 7240,
    prob: 0.97,
    anomScore: -0.53,
    isAnom: true,
    clDbscan: 1,
    clAgg: 0,
    clRisk: 1,
    distUrban: 0,
    lastTested: "2022-08-30",
    priority: 4,
  },
  {
    id: "RJ-JAI-003",
    station: "Jaipur Rural Sanganer",
    state: "rajasthan",
    district: "jaipur",
    lat: 26.82,
    lon: 75.8,
    gwl: 22.0,
    ec: 2840,
    prob: 0.49,
    anomScore: -0.06,
    isAnom: false,
    clDbscan: 4,
    clAgg: 2,
    clRisk: 1,
    distUrban: 1,
    lastTested: "2024-03-01",
    priority: 8,
  },
  {
    id: "RJ-KOT-004",
    station: "Kota Chambal Valley East",
    state: "rajasthan",
    district: "kota",
    lat: 25.18,
    lon: 75.83,
    gwl: 14.5,
    ec: 1910,
    prob: 0.27,
    anomScore: 0.09,
    isAnom: false,
    clDbscan: 4,
    clAgg: 2,
    clRisk: 0,
    distUrban: 1,
    lastTested: "2024-04-12",
    priority: null,
  },
  {
    id: "RJ-UDA-005",
    station: "Udaipur Lake Basin West",
    state: "rajasthan",
    district: "udaipur",
    lat: 24.5854,
    lon: 73.7125,
    gwl: 8.7,
    ec: 1240,
    prob: 0.11,
    anomScore: 0.16,
    isAnom: false,
    clDbscan: 4,
    clAgg: 2,
    clRisk: 0,
    distUrban: 1,
    lastTested: "2024-05-01",
    priority: null,
  },
  {
    id: "WB-N24-001",
    station: "Barasat Gangetic Alluvium",
    state: "west bengal",
    district: "north 24 pgs",
    lat: 22.7234,
    lon: 88.4811,
    gwl: 3.2,
    ec: 1140,
    prob: 0.09,
    anomScore: 0.18,
    isAnom: false,
    clDbscan: 8,
    clAgg: 6,
    clRisk: 0,
    distUrban: 1,
    lastTested: "2024-05-22",
    priority: null,
  },
  {
    id: "WB-MUR-002",
    station: "Murshidabad Bhagirathi Plain",
    state: "west bengal",
    district: "murshidabad",
    lat: 24.1759,
    lon: 88.2802,
    gwl: 4.1,
    ec: 890,
    prob: 0.06,
    anomScore: 0.25,
    isAnom: false,
    clDbscan: 8,
    clAgg: 6,
    clRisk: 0,
    distUrban: 0,
    lastTested: "2024-06-05",
    priority: null,
  },
  {
    id: "WB-NAD-003",
    station: "Nadia Ranaghat Sub-basin",
    state: "west bengal",
    district: "nadia",
    lat: 23.18,
    lon: 88.58,
    gwl: 2.9,
    ec: 3450,
    prob: 0.69,
    anomScore: -0.12,
    isAnom: true,
    clDbscan: 9,
    clAgg: 7,
    clRisk: 1,
    distUrban: 0,
    lastTested: "2023-10-08",
    priority: 6,
  },
  {
    id: "GJ-AHM-001",
    station: "Ahmedabad Sabarmati Basin",
    state: "gujarat",
    district: "ahmedabad",
    lat: 23.0225,
    lon: 72.5714,
    gwl: 7.5,
    ec: 4950,
    prob: 0.89,
    anomScore: -0.33,
    isAnom: true,
    clDbscan: 0,
    clAgg: 8,
    clRisk: 1,
    distUrban: 1,
    lastTested: "2023-07-14",
    priority: 7,
  },
  {
    id: "GJ-SUR-002",
    station: "Surat Coastal Plain",
    state: "gujarat",
    district: "surat",
    lat: 21.1702,
    lon: 72.8311,
    gwl: 4.8,
    ec: 2620,
    prob: 0.42,
    anomScore: -0.04,
    isAnom: false,
    clDbscan: 0,
    clAgg: 8,
    clRisk: 1,
    distUrban: 1,
    lastTested: "2024-02-28",
    priority: 9,
  },
  {
    id: "GJ-KUT-003",
    station: "Kutch Rann Fringe Deep",
    state: "gujarat",
    district: "kutch",
    lat: 23.7337,
    lon: 69.8597,
    gwl: 28.3,
    ec: 8200,
    prob: 0.98,
    anomScore: -0.62,
    isAnom: true,
    clDbscan: -1,
    clAgg: 8,
    clRisk: 1,
    distUrban: 0,
    lastTested: "2021-11-01",
    priority: 12,
  },
];

function deriveWell(r: (typeof RAW_WELLS)[0]): Well {
  const rl = ecToRiskLevel(r.ec, r.prob);
  const depCat = gwlToDepthCategory(r.gwl);
  return {
    id: r.id,
    station: r.station,
    state: r.state,
    district: r.district,
    latitude: r.lat,
    longitude: r.lon,
    groundwaterLevelM: r.gwl,
    gwDepthCategory: depCat,
    isContaminated: r.ec !== null ? r.ec > 3000 : null,
    ecValue: r.ec,
    contaminationProbability: r.prob,
    clusterDbscan: r.clDbscan,
    clusterAgg: r.clAgg,
    anomalyScore: r.anomScore,
    isAnomaly: r.isAnom,
    bbnClusterRisk: r.clRisk as 0 | 1,
    bbnDistrictUrban: r.distUrban as 0 | 1,
    uncertaintySamplingScore:
      r.priority !== null ? Number((1 - Math.abs(r.prob - 0.5) * 2).toFixed(3)) : null,
    testingPriority: r.priority,
    lastTestedDate: r.lastTested,
    riskLevel: rl,
    status: r.ec === null ? "untested" : r.ec > 3000 ? "contaminated" : "clean",
  };
}

const LIVE_WELLS: Well[] = (livePipelineData?.sampleWells || []) as unknown as Well[];
export const MOCK_WELLS: Well[] = LIVE_WELLS.length > 0 ? LIVE_WELLS : RAW_WELLS.map(deriveWell);

// ─── Live Ground-Truth Pipeline Dashboard KPIs ──────────────────────────────
export const MOCK_KPIS: DashboardKPIs = livePipelineData?.kpis
  ? (livePipelineData.kpis as DashboardKPIs)
  : {
      totalWells: 36922,
      testedWells: 34810,
      contaminatedWells: 2063,
      contaminationRate: 0.0559,
      anomaliesDetected: 1749,
      criticalRiskWells: 1420,
      pendingTestQueue: 50,
      lastPipelineRun: "2024-07-01T08:30:00Z",
      statesMonitored: 5,
    };

// ─── Regional Breakdown ──────────────────────────────────────────────────────
export interface RegionalStat {
  state: string;
  stateCode: string;
  totalWells: number;
  contaminated: number;
  contaminationRate: number;
  anomalies: number;
  avgGwl: number;
  avgEc: number;
}

export const MOCK_REGIONAL_STATS: RegionalStat[] = (
  livePipelineData?.regionalStats?.length
    ? livePipelineData.regionalStats
    : [
        {
          state: "Maharashtra",
          stateCode: "MH",
          totalWells: 18268,
          contaminated: 894,
          contaminationRate: 0.0489,
          anomalies: 842,
          avgGwl: 10.4,
          avgEc: 1420,
        },
        {
          state: "Andhra Pradesh",
          stateCode: "AP",
          totalWells: 11014,
          contaminated: 681,
          contaminationRate: 0.0618,
          anomalies: 512,
          avgGwl: 7.2,
          avgEc: 1850,
        },
        {
          state: "West Bengal",
          stateCode: "WB",
          totalWells: 7640,
          contaminated: 488,
          contaminationRate: 0.0639,
          anomalies: 395,
          avgGwl: 3.8,
          avgEc: 1120,
        },
      ]
) as RegionalStat[];

// ─── Risk Distribution ───────────────────────────────────────────────────────
export const MOCK_RISK_DISTRIBUTION = [
  { name: "Low Risk (<15%)", count: 28450, percentage: 77.1, color: "#10b981" },
  { name: "Medium Risk (15-40%)", count: 4989, percentage: 13.5, color: "#3b82f6" },
  { name: "High Risk (40-70%)", count: 2063, percentage: 5.6, color: "#f59e0b" },
  { name: "Critical Risk (>70%)", count: 1420, percentage: 3.8, color: "#dc2626" },
];

// ─── Priority Testing Queue (Active Learning Output) ─────────────────────────
export const MOCK_TESTING_QUEUE: TestingQueueEntry[] = (
  livePipelineData?.testingQueue?.length
    ? livePipelineData.testingQueue.map((item: any) => ({
        rank: item.priorityRank,
        well: item.well as Well,
        uncertaintyScore: item.epistemicUncertainty ?? 0.85,
        bbnContaminationProbability: item.bbnContaminationProbability ?? item.well?.bbnContaminationProbability ?? 0.24,
        reasonFlags: [
          item.epistemicUncertainty > 0.8 ? "high_uncertainty" : "shallow_depth",
          item.well?.isAnomaly ? "anomaly_flagged" : "urban_district",
          item.well?.bbnClusterRisk ? "high_risk_cluster" : "urban_district",
        ] as TestingReason[],
      }))
    : [
        {
          rank: 1,
          well: MOCK_WELLS[0] || RAW_WELLS.map(deriveWell)[0],
          uncertaintyScore: 0.94,
          bbnContaminationProbability: 0.76,
          reasonFlags: ["high_uncertainty", "anomaly_flagged", "high_risk_cluster", "urban_district"],
        },
      ]
) as TestingQueueEntry[];

// ─── Query Helpers ───────────────────────────────────────────────────────────
export function getWells(filters?: WellFilter): Well[] {
  let list = [...MOCK_WELLS];
  if (!filters) return list;

  if (filters.state) {
    list = list.filter((w) => w.state.toLowerCase() === filters.state!.toLowerCase());
  }
  if (filters.district) {
    list = list.filter((w) => w.district.toLowerCase() === filters.district!.toLowerCase());
  }
  if (filters.riskLevel) {
    list = list.filter((w) => w.riskLevel === filters.riskLevel);
  }
  if (filters.status) {
    list = list.filter((w) => w.status === filters.status);
  }
  if (filters.isAnomaly !== undefined) {
    list = list.filter((w) => w.isAnomaly === filters.isAnomaly);
  }
  if (filters.search) {
    const q = filters.search.toLowerCase();
    list = list.filter(
      (w) =>
        w.station.toLowerCase().includes(q) ||
        w.id.toLowerCase().includes(q) ||
        w.district.toLowerCase().includes(q) ||
        w.state.toLowerCase().includes(q)
    );
  }
  return list;
}

export function getWellById(id: string): Well | undefined {
  return MOCK_WELLS.find((w) => w.id.toLowerCase() === id.toLowerCase());
}
