// Small utilities for result rendering – localized to the workspace UI

import { humanSize } from "@/lib/utils";

/** Normalize warning entries into an array of display strings */
export function normalizeWarnings(warnings: any[]): string[] {
  if (!Array.isArray(warnings)) return [];
  return warnings.map((w) => {
    if (typeof w === "string") return w;
    if (w && typeof w === "object") {
      if (typeof w.message === "string") return w.message;
      if (typeof w.code === "string") return `${w.code}: ${w.message ?? ""}`.trim();
    }
    return String(w);
  });
}

/** Extract the most useful error message from a backend error payload */
export function extractErrorMessage(error: any): string {
  if (!error) return "";
  if (typeof error === "string") return error;
  if (error && typeof error === "object") {
    if (typeof error.message === "string") return error.message;
    if (typeof error.detail === "string") return error.detail;
    if (error.code) return `${error.code}: ${error.message ?? ""}`.trim();
    // fallback to JSON stringification (shortened)
    try {
      return JSON.stringify(error);
    } catch {
      return String(error);
    }
  }
  return String(error);
}

/** Human‑readable label for known result_meta keys */
const META_LABELS: Record<string, string> = {
  original_size_bytes: "Original size",
  compressed_size_bytes: "Compressed size",
  reduction_percent: "Reduction",
  page_count: "Page count",
  extracted_char_count: "Characters extracted",
  generated_file_count: "Generated files",
  ocr_confidence: "OCR confidence",
  file_count: "File count",
  image_count: "Image count",
};

/** Format a value for display in the Details section */
function formatValue(key: string, value: any): string {
  if (value == null) return "-";
  if (typeof value === "number") {
    // size bytes
    if (key.toLowerCase().includes("size") && key.toLowerCase().includes("bytes")) {
      return humanSize(value);
    }
    // percentages
    if (key.toLowerCase().includes("percent")) {
      return `${value}%`;
    }
    return String(value);
  }
  if (Array.isArray(value)) {
    return value.map((v) => String(v)).join(", ");
  }
  if (typeof value === "boolean") {
    return value ? "Yes" : "No";
  }
  return String(value);
}

/** Convert result_meta into an array of {label, value} for UI */
export function formatResultMeta(meta: Record<string, any> = {}): { label: string; value: string }[] {
  return Object.entries(meta).map(([k, v]) => {
    const label = META_LABELS[k] ?? k.replace(/_/g, " ").replace(/^(.)/, (m) => m.toUpperCase());
    return { label, value: formatValue(k, v) };
  });
}
