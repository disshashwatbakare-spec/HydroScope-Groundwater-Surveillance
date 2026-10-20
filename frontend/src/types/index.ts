// ─── HydroScope Domain Types ───────────────────────────────────────────────
// Mirrors the actual pipeline outputs from the ML backend.

export type StateCode = "mh" | "rj" | "ap" | "wb" | "gj";

export type ContaminationStatus = "contaminated" | "clean" | "untested";

export type RiskLevel = "critical" | "high" | "medium" | "low";

export type WellDepthCategory = "shallow" | "medium" | "deep";

export type AnomalyStatus = "anomalous" | "normal" | "unscored";

// ─── Well ─────────────────────────────────────────────────────────────────────
export interface Well {
  id: string;
  station: string;
  state: string;
  district: string;
  latitude: number;
  longitude: number;
  groundwaterLevelM: number | null;
  gwDepthCategory: WellDepthCategory;

  // Classification outputs
  isContaminated: boolean | null;
  ecValue: number | null;
  contaminationProbability: number | null;

  // Clustering
  clusterDbscan: number;
  clusterAgg: number;

  // Anomaly detection
  anomalyScore: number | null;
  isAnomaly: boolean;

  // Bayesian features
  bbnClusterRisk: 0 | 1;
  bbnDistrictUrban: 0 | 1;

  // Active learning
  uncertaintySamplingScore: number | null;
  testingPriority: number | null;
  lastTestedDate: string | null;

  // Derived
  riskLevel: RiskLevel;
  status: ContaminationStatus;
}

// ─── Cluster ──────────────────────────────────────────────────────────────────
export interface Cluster {
  id: number;
  method: "dbscan" | "agglomerative";
  wellCount: number;
  contaminationRate: number;
  meanLat: number;
  meanLon: number;
  meanGwl: number;
  riskLevel: RiskLevel;
}

// ─── Model Results ────────────────────────────────────────────────────────────
export interface ModelResult {
  name: string;
  rocAuc: number;
  avgPrecision: number;
  rocCurve: { fpr: number; tpr: number }[];
  prCurve: { recall: number; precision: number }[];
  confusionMatrix: { tn: number; fp: number; fn: number; tp: number };
  classificationReport: { precision: number; recall: number; f1: number; support: number };
}

export interface CostBenefitPoint {
  threshold: number;
  totalCost: number;
}

// ─── Clustering Metrics ───────────────────────────────────────────────────────
export interface ClusteringMetrics {
  dbscanNClusters: number;
  dbscanNoisePct: number;
  dbscanSilhouette: number;
  aggNClusters: number;
  aggSilhouette: number;
}

// ─── Dashboard KPIs ───────────────────────────────────────────────────────────
export interface DashboardKPIs {
  totalWells: number;
  testedWells: number;
  contaminatedWells: number;
  contaminationRate: number;
  anomaliesDetected: number;
  criticalRiskWells: number;
  pendingTestQueue: number;
  lastPipelineRun: string;
  statesMonitored: number;
}

// ─── Active Learning / Testing Queue ─────────────────────────────────────────
export interface TestingQueueEntry {
  rank: number;
  well: Well;
  uncertaintyScore: number;
  bbnContaminationProbability: number;
  reasonFlags: TestingReason[];
}

export type TestingReason =
  | "high_uncertainty"
  | "anomaly_flagged"
  | "high_risk_cluster"
  | "shallow_depth"
  | "urban_district"
  | "long_untested";

// ─── Filters / Pagination ─────────────────────────────────────────────────────
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
}

export interface WellFilter {
  state?: string;
  district?: string;
  riskLevel?: RiskLevel;
  status?: ContaminationStatus;
  isAnomaly?: boolean;
  search?: string;
}
