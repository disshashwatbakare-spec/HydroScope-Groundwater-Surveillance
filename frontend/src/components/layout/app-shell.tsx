"use client";

import * as React from "react";
import { Sidebar } from "./sidebar";
import { Header } from "./header";

interface AppShellProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
}

export function AppShell({ children, title, subtitle }: AppShellProps) {
  return (
    <div
      className="min-h-screen flex bg-[#080E1A] text-slate-100"
      style={{
        backgroundImage: `radial-gradient(ellipse at 50% 0%, rgba(37, 99, 235, 0.08) 0%, transparent 60%), radial-gradient(circle, rgba(255, 255, 255, 0.04) 1px, transparent 1px)`,
        backgroundSize: "100% 100%, 24px 24px",
      }}
    >
      {/* Fixed Left Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex flex-1 flex-col pl-64 min-w-0">
        <Header title={title} subtitle={subtitle} />
        <main className="flex-1 p-6 md:p-8 max-w-[1400px] w-full mx-auto space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
}
