"use client";

import * as React from "react";
import type { Well } from "@/types";
import { formatNumber } from "@/lib/utils";

interface GroundwaterMapProps {
  wells: Well[];
  selectedWell: Well | null;
  onSelectWell: (well: Well) => void;
  showAnomaliesOnly: boolean;
  showClusters: boolean;
}

export function GroundwaterMap({
  wells,
  selectedWell,
  onSelectWell,
  showAnomaliesOnly,
  showClusters,
}: GroundwaterMapProps) {
  const mapContainerRef = React.useRef<HTMLDivElement>(null);
  const mapInstanceRef = React.useRef<any>(null);
  const markersRef = React.useRef<any[]>([]);

  // Dynamically load Leaflet on client-side
  React.useEffect(() => {
    let isCancelled = false;

    async function initMap() {
      if (!mapContainerRef.current) return;
      if (mapInstanceRef.current) return;

      const L = await import("leaflet");
      // Import leaflet css
      if (!document.getElementById("leaflet-css")) {
        const link = document.createElement("link");
        link.id = "leaflet-css";
        link.rel = "stylesheet";
        link.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
        document.head.appendChild(link);
      }

      if (isCancelled || !mapContainerRef.current) return;

      // Center over central India (Lat: 21.0, Lon: 78.5)
      const map = L.map(mapContainerRef.current, {
        center: [21.5, 78.0],
        zoom: 5.5,
        zoomControl: true,
      });

      // Free open-source basemap (OpenStreetMap) — No API key required
      L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
          attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
          maxZoom: 19,
        }
      ).addTo(map);

      mapInstanceRef.current = map;
      renderMarkers(L, map);
    }

    initMap();

    return () => {
      isCancelled = true;
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  const isDirectMarkerClickRef = React.useRef(false);

  // Update markers when wells, selectedWell, or filters change
  const renderMarkers = React.useCallback(
    async (LModule?: any, mapInst?: any) => {
      const L = LModule || (await import("leaflet"));
      const map = mapInst || mapInstanceRef.current;
      if (!map) return;

      // Clear existing markers
      markersRef.current.forEach((m) => m.remove());
      markersRef.current = [];

      const filtered = showAnomaliesOnly ? wells.filter((w) => w.isAnomaly) : wells;

      filtered.forEach((well) => {
        const isSelected = selectedWell?.id === well.id;
        const color =
          well.riskLevel === "critical"
            ? "#dc2626"
            : well.riskLevel === "high"
            ? "#f59e0b"
            : well.riskLevel === "medium"
            ? "#3b82f6"
            : "#10b981";

        const marker = L.circleMarker([well.latitude, well.longitude], {
          radius: isSelected ? 9 : well.isAnomaly ? 7 : 5.5,
          fillColor: color,
          color: isSelected ? "#0f172a" : well.isAnomaly ? "#7e22ce" : "#ffffff",
          weight: isSelected ? 2.5 : well.isAnomaly ? 2 : 1,
          opacity: 1,
          fillOpacity: 0.9,
        }).addTo(map);

        marker.bindTooltip(
          `<strong>${well.station}</strong><br/>
           <span style="font-family: monospace;">[${well.id}]</span> - ${well.district}, ${well.state}<br/>
           EC: ${well.ecValue ? `${well.ecValue} µS/cm` : "Untested"} | Risk: ${(
            (well.contaminationProbability || 0) * 100
          ).toFixed(0)}%
           ${well.isAnomaly ? `<br/><strong style="color: #7e22ce;">Isolation Forest Anomaly</strong>` : ""}`,
          { direction: "top", offset: [0, -6], className: "carto-tooltip" }
        );

        marker.on("click", () => {
          isDirectMarkerClickRef.current = true;
          onSelectWell(well);
        });

        markersRef.current.push(marker);
      });
    },
    [wells, selectedWell, showAnomaliesOnly, onSelectWell]
  );

  React.useEffect(() => {
    if (mapInstanceRef.current) {
      renderMarkers();
    }
  }, [renderMarkers]);

  // Center on selected well if changed from sidebar or external link
  React.useEffect(() => {
    if (!mapInstanceRef.current || !selectedWell) return;
    if (isDirectMarkerClickRef.current) {
      // Direct click on marker: keep user's current zoom and position
      isDirectMarkerClickRef.current = false;
      return;
    }
    // Selection from sidebar list or external button: smooth pan without jarring zoom jump
    mapInstanceRef.current.panTo([selectedWell.latitude, selectedWell.longitude], {
      animate: true,
      duration: 0.8,
    });
  }, [selectedWell]);

  return (
    <div className="relative h-full w-full rounded-lg border border-slate-200 overflow-hidden bg-slate-100">
      <div ref={mapContainerRef} className="h-full w-full" />
    </div>
  );
}
