"use client";

import { ToolCategory, ToolDefinition } from "@/types/tool";
import { CATEGORY_META } from "@/config/categories";
import { cn } from "@/lib/utils";

interface Props {
  tools: ToolDefinition[];
  selectedToolId: string | null;
  categories: ToolCategory[];
  onSelect: (id: string | null) => void;
}

export default function ToolSelector({
  tools,
  selectedToolId,
  categories,
  onSelect,
}: Props) {
  return (
    <div className="space-y-3">
      {categories.map((cat) => {
        const items = tools.filter((t) => t.category === cat);
        if (items.length === 0) return null;
        return (
          <div key={cat}>
            <div className="mb-1.5 text-[11px] font-semibold uppercase tracking-wide text-slate-400">
              {CATEGORY_META[cat].label}
            </div>
            <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
              {items.map((tool) => {
                const active = tool.id === selectedToolId;
                return (
                  <button
                    key={tool.id}
                    onClick={() => onSelect(active ? null : tool.id)}
                    className={cn(
                      "rounded-xl border p-3 text-left transition-colors",
                      active
                        ? "border-brand-500 bg-brand-50 ring-1 ring-brand-200"
                        : "border-slate-200 bg-white hover:border-brand-200 hover:bg-slate-50"
                    )}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-slate-900">
                        {tool.label}
                      </span>
                      <span className="text-[10px] uppercase text-slate-400">
                        → {tool.outputType}
                      </span>
                    </div>
                    <p className="mt-1 text-xs text-slate-500">
                      {tool.description}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}