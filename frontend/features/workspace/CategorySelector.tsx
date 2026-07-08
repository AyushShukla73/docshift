"use client";

import { useMemo } from "react";
import { ToolDefinition, ToolCategory } from "@/types/tool";
import { CATEGORY_META, CATEGORY_ORDER } from "@/config/categories";
import { cn } from "@/lib/utils";

interface Props {
  tools: ToolDefinition[];
  selectedToolId: string | null;
  onSelect: (id: string | null) => void;
}

export default function CategorySelector({
  tools,
  selectedToolId,
  onSelect,
}: Props) {
  const byCategory = useMemo(() => {
    const map = new Map<ToolCategory, ToolDefinition[]>();
    for (const cat of CATEGORY_ORDER) map.set(cat, []);
    for (const t of tools) {
      map.get(t.category)?.push(t);
    }
    return map;
  }, [tools]);

  const selectedTool = tools.find((t) => t.id === selectedToolId) ?? null;
  const activeCategory = selectedTool?.category ?? null;

  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
      {CATEGORY_ORDER.map((cat) => {
        const count = byCategory.get(cat)?.length ?? 0;
        const meta = CATEGORY_META[cat];
        const isActive = activeCategory === cat;
        const disabled = count === 0;
        return (
          <div
            key={cat}
            className={cn(
              "rounded-xl border p-3 transition-colors",
              isActive
                ? "border-brand-300 bg-brand-50"
                : "border-slate-200 bg-white",
              disabled && "opacity-50"
            )}
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wide text-slate-700">
                {meta.label}
              </span>
              <span className="rounded-full bg-slate-100 px-1.5 text-[10px] font-medium text-slate-600">
                {count}
              </span>
            </div>
            <p className="mt-1 text-[11px] text-slate-500">{meta.description}</p>
          </div>
        );
      })}
    </div>
  );
}