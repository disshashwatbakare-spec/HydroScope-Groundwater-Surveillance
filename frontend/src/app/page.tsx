"use client";

import * as React from "react";
import Link from "next/link";
import {
  MapPin,
  Droplets,
  Activity,
  BarChart3,
  Network,
  FlaskConical,
  ArrowRight,
  CheckCircle2,
  AlertTriangle,
  Globe,
  TrendingUp,
  Zap,
  ShieldCheck,
  ChevronRight,
  Waves,
  Menu,
  X,
  ExternalLink,
  Users,
  Database,
  Cpu,
} from "lucide-react";

const PHASE_STYLES: Record<
  string,
  { wrap: string; icon: string; label: string; badge: string }
> = {
  blue: {
    wrap: "bg-blue-600/20 border-blue-500/30",
    icon: "text-blue-400",
    label: "text-blue-400",
    badge: "border-blue-500/20 bg-blue-950/60 text-blue-300",
  },
  teal: {
    wrap: "bg-teal-600/20 border-teal-500/30",
    icon: "text-teal-400",
    label: "text-teal-400",
    badge: "border-teal-500/20 bg-teal-950/60 text-teal-300",
  },
  violet: {
    wrap: "bg-violet-600/20 border-violet-500/30",
    icon: "text-violet-400",
    label: "text-violet-400",
    badge: "border-violet-500/20 bg-violet-950/60 text-violet-300",
  },
  rose: {
    wrap: "bg-rose-600/20 border-rose-500/30",
    icon: "text-rose-400",
    label: "text-rose-400",
    badge: "border-rose-500/20 bg-rose-950/60 text-rose-300",
  },
  emerald: {
    wrap: "bg-emerald-600/20 border-emerald-500/30",
    icon: "text-emerald-400",
    label: "text-emerald-400",
    badge: "border-emerald-500/20 bg-emerald-950/60 text-emerald-300",
  },
  indigo: {
    wrap: "bg-indigo-600/20 border-indigo-500/30",
    icon: "text-indigo-400",
    label: "text-indigo-400",
    badge: "border-indigo-500/20 bg-indigo-950/60 text-indigo-300",
  },
};

const CHECK_COLOR: Record<string, string> = {
  blue: "text-blue-400",
  teal: "text-teal-400",
  violet: "text-violet-400",
  indigo: "text-indigo-400",
  emerald: "text-emerald-400",
};

const PROBLEM_ICON: Record<string, string> = {
  rose: "text-rose-400 bg-rose-500/15 border-rose-500/30",
  amber: "text-amber-400 bg-amber-500/15 border-amber-500/30",
  orange: "text-orange-400 bg-orange-500/15 border-orange-500/30",
  violet: "text-violet-400 bg-violet-500/15 border-violet-500/30",
};

const RESULT_ICON: Record<string, string> = {
  blue: "text-blue-400 bg-blue-500/15 border-blue-500/30",
  emerald: "text-emerald-400 bg-emerald-500/15 border-emerald-500/30",
  rose: "text-rose-400 bg-rose-500/15 border-rose-500/30",
  violet: "text-violet-400 bg-violet-500/15 border-violet-500/30",
  teal: "text-teal-400 bg-teal-500/15 border-teal-500/30",
  indigo: "text-indigo-400 bg-indigo-500/15 border-indigo-500/30",
};

// ─── Navigation ───────────────────────────────────────────────────────────────
function Navbar() {
  const [open, setOpen] = React.useState(false);
  const [scrolled, setScrolled] = React.useState(false);

  React.useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-[#080E1A]/95 backdrop-blur-xl border-b border-white/8 shadow-lg shadow-black/20"
          : "bg-transparent"
      }`}
    >
      <div className="mx-auto max-w-7xl px-6 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600/20 border border-blue-500/30">
            <Waves className="h-4 w-4 text-blue-400" />
          </div>
          <span className="text-white font-semibold text-sm tracking-tight">HydroScope</span>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-8">
          {[
            { label: "Problem", href: "#problem" },
            { label: "Solution", href: "#solution" },
            { label: "Features", href: "#features" },
            { label: "How It Works", href: "#pipeline" },
            { label: "Results", href: "#results" },
          ].map((item) => (
            <a
              key={item.label}
              href={item.href}
              className="text-sm text-slate-300 hover:text-white transition-colors"
            >
              {item.label}
            </a>
          ))}
        </div>

        {/* CTA */}
        <div className="hidden md:flex items-center gap-3">
          <Link href="/about">
            <span className="text-sm text-slate-300 hover:text-white transition-colors cursor-pointer">
              About
            </span>
          </Link>
          <Link href="/dashboard">
            <button className="flex items-center gap-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold px-4 py-2 transition-colors">
              Open Dashboard
              <ArrowRight className="h-3.5 w-3.5 text-white" />
            </button>
          </Link>
        </div>

        {/* Mobile Menu Toggle */}
        <button
          onClick={() => setOpen(!open)}
          className="md:hidden text-white/70 hover:text-white"
        >
          {open ? <X className="h-5 w-5 text-white" /> : <Menu className="h-5 w-5 text-white" />}
        </button>
      </div>

      {/* Mobile Menu */}
      {open && (
        <div className="md:hidden bg-[#080E1A]/98 border-b border-white/8 px-6 py-4 space-y-3">
          {["Problem", "Solution", "Features", "Pipeline", "Results"].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              onClick={() => setOpen(false)}
              className="block text-sm text-slate-300 hover:text-white py-1.5"
            >
              {item}
            </a>
          ))}
          <Link href="/dashboard" onClick={() => setOpen(false)}>
            <button className="w-full mt-2 rounded-lg bg-blue-600 text-white text-sm font-semibold px-4 py-2.5">
              Open Dashboard
            </button>
          </Link>
        </div>
      )}
    </nav>
  );
}

// ─── Hero Section ─────────────────────────────────────────────────────────────
function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#080E1A]">
      {/* Background layers */}
      <div
        className="absolute inset-0 opacity-30"
        style={{
          backgroundImage:
            "radial-gradient(ellipse 80% 50% at 50% -20%, rgba(37,99,235,0.35), transparent)",
        }}
      />
      <div
        className="absolute inset-0 opacity-15"
        style={{
          backgroundImage:
            "radial-gradient(circle, rgba(99,102,241,1) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }}
      />
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-[#080E1A] to-transparent" />

      <div className="relative z-10 mx-auto max-w-7xl px-6 pt-24 pb-16 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-1.5 text-xs font-semibold text-blue-300 mb-8">
          <span className="h-1.5 w-1.5 rounded-full bg-blue-400 animate-pulse" />
          ML Research · MIT-WPU Semester V · India
        </div>

        {/* Headline */}
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-white tracking-tight leading-[1.05] max-w-5xl mx-auto">
          AI-Powered{" "}
          <span className="text-blue-400">
            Groundwater
          </span>
          <br />
          Contamination Surveillance
        </h1>

        <p className="mt-6 text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
          A 4-phase machine learning system monitoring{" "}
          <strong className="text-white/80">36,922 wells</strong> across{" "}
          <strong className="text-white/80">5 Indian states</strong> — classifying
          contamination risk, clustering hydro-geological zones, detecting anomalies, and
          allocating lab tests intelligently using a Bayesian Belief Network.
        </p>

        {/* CTAs */}
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <Link href="/dashboard">
            <button className="flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold px-7 py-3.5 text-sm transition-all hover:scale-[1.02] shadow-lg shadow-blue-900/40">
              <BarChart3 className="h-4 w-4 text-white" />
              Open Live Dashboard
              <ArrowRight className="h-4 w-4 text-white" />
            </button>
          </Link>
          <Link href="/about">
            <button className="flex items-center gap-2 rounded-xl border border-white/15 bg-white/5 hover:bg-white/10 text-white/80 hover:text-white font-semibold px-7 py-3.5 text-sm transition-all">
              <ExternalLink className="h-4 w-4 text-slate-200" />
              Read the Deep-Dive
            </button>
          </Link>
        </div>

        {/* Impact Numbers */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-px bg-white/8 rounded-2xl overflow-hidden border border-white/8 max-w-3xl mx-auto">
          {[
            { value: "36,922", label: "Wells Monitored" },
            { value: "0.922", label: "RF ROC-AUC" },
            { value: "+86.4%", label: "Detection Gain" },
            { value: "5 States", label: "MH · AP · WB · RJ · GJ" },
          ].map((s, i) => (
            <div key={i} className="bg-white/4 hover:bg-white/6 transition-colors px-6 py-5 text-center">
              <div className="text-2xl font-bold font-mono text-white tracking-tight">{s.value}</div>
              <div className="text-xs text-slate-400 mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ─── Problem Section ──────────────────────────────────────────────────────────
function ProblemSection() {
  const crisisStats = [
    { value: "600M+", label: "Indians at risk from contaminated groundwater", color: "rose" },
    { value: "36,922", label: "Wells needing monitoring — with only 50 lab kits/month", color: "amber" },
    { value: "5.59%", label: "Contamination rate — undetectable by eye or inspection alone", color: "orange" },
    { value: "738×", label: "More wells than budget — without AI, most go untested indefinitely", color: "red" },
  ];

  return (
    <section id="problem" className="bg-[#080E1A] py-24 px-6 relative border-t border-white/6 overflow-hidden">
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: "radial-gradient(ellipse 60% 40% at 20% 40%, rgba(244,63,94,0.12), transparent)",
        }}
      />
      <div className="relative z-10 mx-auto max-w-7xl">
        {/* Section label */}
        <div className="flex items-center gap-2 mb-5">
          <div className="h-px w-8 bg-rose-400" />
          <span className="text-xs font-bold uppercase tracking-widest text-rose-400">The Problem</span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold text-white leading-tight tracking-tight">
              India's groundwater crisis is silent, slow, and{" "}
              <span className="text-rose-400">catastrophically under-monitored</span>
            </h2>
            <p className="mt-5 text-slate-300 leading-relaxed text-[15px]">
              Groundwater provides{" "}
              <strong className="text-white">over 85% of rural India's drinking water</strong>. Yet contamination from
              industrial discharge, agricultural runoff, and natural geological salinity goes
              undetected for years — because identifying which wells to test requires expert
              knowledge, geographic reach, and resources that simply don't exist at scale.
            </p>
            <p className="mt-4 text-slate-400 leading-relaxed text-[15px]">
              The Central Ground Water Board (CGWB) maintains data on tens of thousands of
              monitoring stations across India. The core problem isn't <em>data availability</em> —
              it's the <strong className="text-white">intelligent extraction of actionable insight</strong> from it.
            </p>

            {/* Key Challenges */}
            <div className="mt-8 space-y-4">
              {[
                {
                  title: "Extreme Class Imbalance",
                  desc: "Only 5.59% of wells exceed safe EC thresholds (>3,000 µS/cm). Naive ML classifiers trained on this distribution predict 'clean' 95% of the time and appear 94% accurate — while missing virtually every contaminated well.",
                  icon: AlertTriangle,
                  color: "rose",
                },
                {
                  title: "Budget-Constrained Testing",
                  desc: "With 36,922 monitored stations and a practical budget of ~50 lab tests per month, randomly selecting wells would take over 60 years to cover the full network. Every wrong pick is a missed health risk.",
                  icon: FlaskConical,
                  color: "amber",
                },
                {
                  title: "Geographic Blind Spots",
                  desc: "Standard classifiers trained globally miss local anomalies — a single highly polluted well in a predominantly clean cluster gets diluted and overlooked. Local context is everything.",
                  icon: MapPin,
                  color: "orange",
                },
                {
                  title: "No Prioritization Intelligence",
                  desc: "Without a ranking system that weighs ML predictions, spatial clusters, anomaly scores, and prior probabilities together, field teams have no systematic basis to decide which wells to visit next.",
                  icon: Database,
                  color: "violet",
                },
              ].map((item, i) => {
                const Icon = item.icon;
                return (
                  <div key={i} className="flex gap-4 p-4 rounded-xl border border-white/8 bg-[#0D1526]/80 backdrop-blur-md hover:border-white/15 transition-all">
                    <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border ${PROBLEM_ICON[item.color] || "text-slate-300 bg-white/5 border-white/10"}`}>
                      <Icon className="h-4 w-4" />
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-white">{item.title}</div>
                      <div className="text-xs text-slate-400 mt-1 leading-relaxed">{item.desc}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right: Crisis stats */}
          <div className="lg:pt-12">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {crisisStats.map((s, i) => (
                <div
                  key={i}
                  className="rounded-2xl border border-white/8 bg-[#0D1526]/80 backdrop-blur-md p-6 shadow-lg shadow-black/20 hover:border-white/15 transition-all"
                >
                  <div className="text-3xl font-bold font-mono text-white tracking-tight">
                    {s.value}
                  </div>
                  <div className="mt-2 text-xs text-slate-400 leading-relaxed">{s.label}</div>
                </div>
              ))}
            </div>

            {/* States coverage map visual */}
            <div className="mt-6 rounded-2xl border border-white/8 bg-[#0D1526]/90 backdrop-blur-md p-6 overflow-hidden relative shadow-lg shadow-black/20">
              <div
                className="absolute inset-0 opacity-20 pointer-events-none"
                style={{
                  backgroundImage: "radial-gradient(circle, rgba(96,165,250,0.8) 1px, transparent 1px)",
                  backgroundSize: "20px 20px",
                }}
              />
              <div className="relative z-10">
                <div className="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-4">
                  States Covered Under Surveillance
                </div>
                <div className="grid grid-cols-1 gap-2">
                  {[
                    { code: "MH", name: "Maharashtra", wells: "8,240", risk: "High" },
                    { code: "AP", name: "Andhra Pradesh", wells: "9,100", risk: "Critical" },
                    { code: "WB", name: "West Bengal", wells: "7,620", risk: "High" },
                    { code: "RJ", name: "Rajasthan", wells: "6,380", risk: "Critical" },
                    { code: "GJ", name: "Gujarat", wells: "5,582", risk: "Medium" },
                  ].map((state) => (
                    <div
                      key={state.code}
                      className="flex items-center justify-between rounded-lg bg-white/4 hover:bg-white/8 transition-colors px-3 py-2 border border-white/5"
                    >
                      <div className="flex items-center gap-2.5">
                        <span className="text-[10px] font-bold font-mono text-blue-300 bg-blue-500/20 border border-blue-500/30 rounded px-1.5 py-0.5">
                          {state.code}
                        </span>
                        <span className="text-sm text-slate-200">{state.name}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-xs font-mono text-slate-400">{state.wells} wells</span>
                        <span
                          className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${
                            state.risk === "Critical"
                              ? "bg-rose-500/15 text-rose-300 border-rose-500/30"
                              : state.risk === "High"
                              ? "bg-amber-500/15 text-amber-300 border-amber-500/30"
                              : "bg-emerald-500/15 text-emerald-300 border-emerald-500/30"
                          }`}
                        >
                          {state.risk}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// ─── Solution Section ─────────────────────────────────────────────────────────
function SolutionSection() {
  return (
    <section id="solution" className="bg-[#080E1A] py-24 px-6 relative overflow-hidden">
      <div
        className="absolute inset-0 opacity-15"
        style={{
          backgroundImage:
            "radial-gradient(ellipse 60% 40% at 70% 50%, rgba(37,99,235,0.3), transparent)",
        }}
      />
      <div className="relative z-10 mx-auto max-w-7xl">
        <div className="flex items-center gap-2 mb-5">
          <div className="h-px w-8 bg-blue-400" />
          <span className="text-xs font-bold uppercase tracking-widest text-blue-400">The Solution</span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold text-white leading-tight tracking-tight">
              A closed-loop AI pipeline that{" "}
              <span className="text-blue-400">thinks geographically</span> and acts
              within your budget
            </h2>
            <p className="mt-5 text-slate-300 leading-relaxed text-[15px]">
              HydroScope doesn't just classify wells — it understands <em className="text-white">spatial context</em>,
              detects localized outliers within their regional peer group, and then combines all
              signals into a Bayesian probability estimate to produce a{" "}
              <strong className="text-white/80">ranked field dispatch order</strong>.
            </p>
            <p className="mt-4 text-slate-400 leading-relaxed text-[15px]">
              Every one of the 50 monthly lab kits is allocated to the well that maximizes{" "}
              <strong className="text-white/80">information gain</strong> — where ML uncertainty
              is highest, contamination probability is elevated, or local anomaly flags add
              urgency. This is active learning: the more you test, the smarter it gets.
            </p>

            <div className="mt-8 space-y-3">
              {[
                { text: "Handles 94.4% class imbalance with SMOTE synthetic oversampling", color: "blue" },
                { text: "39 DBSCAN spatial clusters for local context-aware detection", color: "teal" },
                { text: "Isolation Forest runs per-cluster, not globally — finding true local anomalies", color: "violet" },
                { text: "Bayesian Belief Network fuses 3 evidence streams into a posterior probability", color: "indigo" },
                { text: "Active learning uncertainty sampling ensures highest information-gain tests first", color: "emerald" },
              ].map((item, i) => (
                <div key={i} className="flex items-start gap-3">
                  <CheckCircle2 className={`h-4 w-4 mt-0.5 shrink-0 ${CHECK_COLOR[item.color] || "text-blue-400"}`} />
                  <span className="text-sm text-slate-300">{item.text}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Solution pipeline visualization */}
          <div className="space-y-3">
            {[
              {
                phase: "01",
                title: "Ingest & Unify",
                desc: "Chemical, physical, and GWL datasets merged by station × district × state × month",
                icon: Database,
                color: "blue",
                output: "36,922 wells unified",
              },
              {
                phase: "02",
                title: "Classify (RF + SMOTE)",
                desc: "Random Forest trained on SMOTE-balanced data. Optimal threshold at 0.35 (not 0.5) minimizes false negatives",
                icon: Cpu,
                color: "teal",
                output: "ROC-AUC 0.9217",
              },
              {
                phase: "03",
                title: "Cluster Spatially",
                desc: "DBSCAN on lat/lon/GWL identifies 39 hydro-geological zones for regional peer comparison",
                icon: MapPin,
                color: "violet",
                output: "39 clusters · Silhouette 0.43",
              },
              {
                phase: "04",
                title: "Detect Anomalies",
                desc: "Isolation Forest within each cluster finds wells deviating from their regional norm — catching what global models miss",
                icon: Activity,
                color: "rose",
                output: "1,749 anomalies (4.74%)",
              },
              {
                phase: "05",
                title: "Prioritize & Dispatch",
                desc: "Bayesian BBN + uncertainty sampling produces a ranked lab-test manifest. Top 50 dispatched each month",
                icon: FlaskConical,
                color: "emerald",
                output: "+86.4% vs random testing",
              },
            ].map((step, i) => {
              const Icon = step.icon;
              const tone = PHASE_STYLES[step.color] || PHASE_STYLES.blue;
              return (
                <div
                  key={i}
                  className="flex items-start gap-4 rounded-xl border border-white/8 bg-white/4 hover:bg-white/6 transition-colors p-4"
                >
                  <div className="flex flex-col items-center gap-1.5 shrink-0">
                    <div className={`flex h-10 w-10 items-center justify-center rounded-xl border ${tone.wrap}`}>
                      <Icon className={`h-4 w-4 ${tone.icon}`} />
                    </div>
                    {i < 4 && <div className="w-px h-3 bg-white/10" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`text-[10px] font-bold font-mono ${tone.label}`}>
                        PHASE {step.phase}
                      </span>
                      <span className="text-sm font-semibold text-white">{step.title}</span>
                    </div>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed">{step.desc}</p>
                  </div>
                  <div className={`shrink-0 rounded-lg border px-2.5 py-1.5 text-[10px] font-semibold text-right whitespace-nowrap ${tone.badge}`}>
                    {step.output}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}

// ─── Features Section ─────────────────────────────────────────────────────────
function FeaturesSection() {
  const features = [
    {
      icon: MapPin,
      title: "Geospatial Risk Map",
      desc: "Interactive Leaflet map with contamination clusters, anomaly hotspots, well depth visualization, and regional boundary overlays. Filter by state, risk level, or cluster ID.",
      href: "/map",
      color: "blue",
    },
    {
      icon: Droplets,
      title: "Well Inventory",
      desc: "Browse, search, and filter all 36,922 monitoring stations. View per-well ML scores — contamination probability, anomaly score, cluster membership, and testing priority.",
      href: "/wells",
      color: "sky",
    },
    {
      icon: FlaskConical,
      title: "Active Testing Queue",
      desc: "Budget-aware lab dispatch interface. See which wells the BBN ranks as highest priority this month, dispatch kit allocations, and track remaining budget.",
      href: "/testing-queue",
      color: "teal",
    },
    {
      icon: BarChart3,
      title: "Model Analytics",
      desc: "ROC curves, precision-recall curves, confusion matrix, cost-benefit analysis, and cluster quality metrics — all from the live pipeline output.",
      href: "/analytics",
      color: "violet",
    },
    {
      icon: Network,
      title: "Bayesian Network Simulator",
      desc: "Interactive BBN interface. Set evidence values (cluster risk, depth, urbanization) and see how posterior contamination probability updates in real-time.",
      href: "/models",
      color: "indigo",
    },
    {
      icon: Activity,
      title: "Anomaly Insights",
      desc: "Explore hydro-geological outliers — wells that deviate from their regional cluster norm in ways that a global classifier would miss entirely.",
      href: "/analytics",
      color: "rose",
    },
  ];

  return (
    <section id="features" className="bg-[#080E1A] py-24 px-6 relative border-t border-white/6 overflow-hidden">
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: "radial-gradient(ellipse 60% 40% at 80% 30%, rgba(37,99,235,0.15), transparent)",
        }}
      />
      <div className="relative z-10 mx-auto max-w-7xl">
        <div className="text-center mb-14">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="h-px w-8 bg-blue-400" />
            <span className="text-xs font-bold uppercase tracking-widest text-blue-400">Platform Features</span>
            <div className="h-px w-8 bg-blue-400" />
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight">
            Everything you need to monitor at scale
          </h2>
          <p className="mt-4 text-slate-400 max-w-xl mx-auto text-sm leading-relaxed">
            Six purpose-built views that translate complex ML outputs into clear,
            actionable information for researchers, field teams, and policymakers.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((f, i) => {
            const Icon = f.icon;
            return (
              <Link key={i} href={f.href} className="group">
                <div className="h-full flex flex-col gap-4 rounded-2xl border border-white/8 bg-[#0D1526]/80 backdrop-blur-md p-6 shadow-lg shadow-black/20 hover:border-white/18 hover:bg-[#0D1526] hover:-translate-y-1 transition-all duration-200">
                  <div className={`flex h-11 w-11 items-center justify-center rounded-xl bg-white/5 border border-white/10 group-hover:border-blue-500/30 transition-colors`}>
                    <Icon className="h-5 w-5 text-blue-400" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-white text-sm group-hover:text-blue-300 transition-colors">
                      {f.title}
                    </h3>
                    <p className="mt-2 text-xs text-slate-400 leading-relaxed">{f.desc}</p>
                  </div>
                  <div className="mt-auto flex items-center gap-1 text-xs font-semibold text-blue-400 group-hover:gap-2 transition-all">
                    <span>Open Feature</span>
                    <ChevronRight className="h-3.5 w-3.5 text-blue-400" />
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </section>
  );
}

// ─── Pipeline Section ─────────────────────────────────────────────────────────
function PipelineSection() {
  return (
    <section id="pipeline" className="bg-[#080E1A] py-24 px-6 relative border-t border-white/6 overflow-hidden">
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: "radial-gradient(ellipse 60% 40% at 30% 50%, rgba(139,92,246,0.15), transparent)",
        }}
      />
      <div className="relative z-10 mx-auto max-w-7xl">
        <div className="text-center mb-14">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="h-px w-8 bg-violet-400" />
            <span className="text-xs font-bold uppercase tracking-widest text-violet-400">How It Works</span>
            <div className="h-px w-8 bg-violet-400" />
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight">
            From raw CGWB records to ranked lab dispatch
          </h2>
        </div>

        {/* Horizontal Pipeline */}
        <div className="overflow-x-auto pb-4">
          <div className="flex items-stretch gap-0 min-w-max mx-auto max-w-5xl">
            {[
              {
                phase: "Phase 1",
                title: "Ingest & Merge",
                color: "blue",
                bg: "bg-blue-600",
                stats: ["36,922 wells", "1961–2025", "5 states"],
                desc: "Chemical EC/pH + Physical GWL records merged by station",
              },
              {
                phase: "Phase 2",
                title: "RF + SMOTE",
                color: "teal",
                bg: "bg-teal-600",
                stats: ["ROC-AUC 0.922", "SMOTE k=5", "Threshold 0.35"],
                desc: "Classification with imbalance handling",
              },
              {
                phase: "Phase 3",
                title: "DBSCAN Clustering",
                color: "violet",
                bg: "bg-violet-600",
                stats: ["39 clusters", "Silhouette 0.43", "eps=0.35"],
                desc: "Spatial hydro-geological zone detection",
              },
              {
                phase: "Phase 4",
                title: "Isolation Forest",
                color: "rose",
                bg: "bg-rose-600",
                stats: ["1,749 anomalies", "4.74% rate", "Per-cluster"],
                desc: "Local outlier detection within peer groups",
              },
              {
                phase: "Output",
                title: "BBN Dispatch",
                color: "emerald",
                bg: "bg-emerald-600",
                stats: ["+86.4% gain", "50 kits/mo", "2.1× lift"],
                desc: "Ranked lab kit allocation via Bayesian inference",
              },
            ].map((step, i) => (
              <React.Fragment key={i}>
                <div className="flex flex-col rounded-xl border border-white/8 bg-[#0D1526]/80 backdrop-blur-md shadow-lg shadow-black/20 p-5 w-48 shrink-0 hover:border-white/18 transition-all">
                  <div className={`inline-flex self-start rounded-lg ${step.bg} px-2.5 py-1 text-[10px] font-bold text-white uppercase tracking-wider mb-3`}>
                    {step.phase}
                  </div>
                  <div className="font-semibold text-white text-sm leading-tight">{step.title}</div>
                  <div className="mt-1 text-[11px] text-slate-400 leading-snug">{step.desc}</div>
                  <div className="mt-4 space-y-1">
                    {step.stats.map((s, j) => (
                      <div key={j} className="text-[11px] font-mono text-slate-300 bg-white/5 border border-white/10 rounded-md px-2 py-0.5">
                        {s}
                      </div>
                    ))}
                  </div>
                </div>
                {i < 4 && (
                  <div className="flex items-center px-2 shrink-0">
                    <ArrowRight className="h-5 w-5 text-slate-400" />
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

// ─── Results Section ──────────────────────────────────────────────────────────
function ResultsSection() {
  return (
    <section id="results" className="bg-[#080E1A] py-24 px-6 relative border-t border-white/6 overflow-hidden">
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage:
            "radial-gradient(ellipse 50% 60% at 20% 50%, rgba(52,211,153,0.25), transparent), radial-gradient(ellipse 40% 50% at 80% 50%, rgba(37,99,235,0.2), transparent)",
        }}
      />
      <div className="relative z-10 mx-auto max-w-7xl">
        <div className="text-center mb-14">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="h-px w-8 bg-emerald-400" />
            <span className="text-xs font-bold uppercase tracking-widest text-emerald-400">Pipeline Results</span>
            <div className="h-px w-8 bg-emerald-400" />
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight">
            Quantified impact — not estimates
          </h2>
          <p className="mt-4 text-slate-400 text-sm max-w-lg mx-auto">
            All metrics computed on held-out CGWB test data. Zero data leakage — spatial features never seen during classifier training.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {[
            {
              value: "0.9217",
              label: "Random Forest ROC-AUC",
              sub: "vs. 0.8926 for KNN baseline",
              icon: TrendingUp,
              color: "blue",
            },
            {
              value: "+86.4%",
              label: "Detection gain over random testing",
              sub: "More contaminated wells found per 50 kits",
              icon: Zap,
              color: "emerald",
            },
            {
              value: "1,749",
              label: "Hydro-geological anomalies found",
              sub: "4.74% of all wells — missed by global models",
              icon: Activity,
              color: "rose",
            },
            {
              value: "0.43",
              label: "DBSCAN Silhouette Score",
              sub: "39 well-separated spatial clusters",
              icon: MapPin,
              color: "violet",
            },
            {
              value: "2.1×",
              label: "Detection multiplier vs baseline",
              sub: "Within identical 50/month testing budget",
              icon: ShieldCheck,
              color: "teal",
            },
            {
              value: "36,922",
              label: "Wells fully scored and ranked",
              sub: "Risk, cluster, anomaly, BBN probability",
              icon: Database,
              color: "indigo",
            },
          ].map((r, i) => {
            const Icon = r.icon;
            const tone = RESULT_ICON[r.color] || "text-slate-200 bg-white/5 border-white/10";
            return (
              <div
                key={i}
                className="rounded-2xl border border-white/8 bg-[#0D1526]/80 backdrop-blur-md hover:border-white/18 transition-all p-6 shadow-lg shadow-black/20"
              >
                <div className={`flex h-10 w-10 items-center justify-center rounded-xl border mb-4 ${tone}`}>
                  <Icon className="h-4 w-4" />
                </div>
                <div className="text-3xl font-bold font-mono text-white tracking-tight">
                  {r.value}
                </div>
                <div className="mt-2 text-sm font-medium text-slate-300">{r.label}</div>
                <div className="mt-1 text-xs text-slate-500">{r.sub}</div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

// ─── CTA Section ──────────────────────────────────────────────────────────────
function CTASection() {
  return (
    <section className="bg-[#080E1A] py-24 px-6 relative border-t border-white/6 overflow-hidden">
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: "radial-gradient(ellipse 60% 40% at 50% 50%, rgba(37,99,235,0.2), transparent)",
        }}
      />
      <div className="relative z-10 mx-auto max-w-3xl text-center">
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-500/10 border border-blue-500/20 mx-auto mb-6 shadow-lg shadow-blue-500/10">
          <Waves className="h-7 w-7 text-blue-400" />
        </div>
        <h2 className="text-3xl md:text-4xl font-bold text-white tracking-tight">
          Explore the live system
        </h2>
        <p className="mt-4 text-slate-400 text-sm leading-relaxed max-w-lg mx-auto">
          The full pipeline is running. Browse the interactive dashboard, explore the geospatial
          risk map, inspect individual wells, and see how the BBN allocates this month's
          50 lab testing kits.
        </p>
        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <Link href="/dashboard">
            <button className="flex items-center gap-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold px-7 py-3.5 text-sm transition-all hover:scale-[1.02] shadow-lg shadow-blue-900/40">
              <BarChart3 className="h-4 w-4 text-white" />
              Open Dashboard
              <ArrowRight className="h-4 w-4 text-white" />
            </button>
          </Link>
          <Link href="/about">
            <button className="flex items-center gap-2 rounded-xl border border-white/15 bg-white/5 hover:bg-white/10 text-white font-semibold px-7 py-3.5 text-sm transition-all">
              <ExternalLink className="h-4 w-4 text-slate-200" />
              Full Technical Deep-Dive
            </button>
          </Link>
        </div>
      </div>
    </section>
  );
}

// ─── Footer ───────────────────────────────────────────────────────────────────
function Footer() {
  return (
    <footer className="bg-[#080E1A] border-t border-white/6 py-12 px-6">
      <div className="mx-auto max-w-7xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600/20 border border-blue-500/30">
              <Waves className="h-4 w-4 text-blue-400" />
            </div>
            <div>
              <div className="text-sm font-semibold text-white">HydroScope</div>
              <div className="text-xs text-slate-400">MIT-WPU · Semester V ML Lab</div>
            </div>
          </div>

          <div className="flex flex-wrap gap-6">
            {[
              { label: "Dashboard", href: "/dashboard" },
              { label: "Geospatial Map", href: "/map" },
              { label: "Well Inventory", href: "/wells" },
              { label: "Testing Queue", href: "/testing-queue" },
              { label: "Analytics", href: "/analytics" },
              { label: "BBN Model", href: "/models" },
              { label: "About", href: "/about" },
            ].map((link) => (
              <Link
                key={link.label}
                href={link.href}
                className="text-xs text-slate-400 hover:text-white transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-white/6 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-xs text-slate-500">
            Data source: Central Ground Water Board (CGWB) · 1961–2025
          </div>
          <div className="text-xs text-slate-500">
            CGWB Chemical · Physical · GWL Datasets · 5 States
          </div>
        </div>
      </div>
    </footer>
  );
}

// ─── Root Page ────────────────────────────────────────────────────────────────
export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#080E1A] text-slate-200" style={{ fontFamily: "var(--font-inter, sans-serif)" }}>
      <Navbar />
      <Hero />
      <ProblemSection />
      <SolutionSection />
      <FeaturesSection />
      <PipelineSection />
      <ResultsSection />
      <CTASection />
      <Footer />
    </div>
  );
}
