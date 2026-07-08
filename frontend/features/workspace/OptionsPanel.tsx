"use client";

import { ToolDefinition } from "@/types/tool";
import { Icon } from "@/components/ui/Icon";

interface Props {
  tool: ToolDefinition | null;
  options: Record<string, unknown>;
  onChange: (next: Record<string, unknown>) => void;
}

export default function OptionsPanel({ tool, options, onChange }: Props) {
  if (!tool) {
    return (
      <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50/50 p-4 text-xs text-slate-500">
        Select a tool to see its options.
      </div>
    );
  }

  if (!tool.configurable) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-4">
        <div className="flex items-center gap-2 text-xs text-slate-600">
          <Icon name="sparkles" className="h-4 w-4 text-brand-600" />
          <span>
            <strong className="text-slate-800">{tool.label}</strong> runs with
            default settings — no options required.
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
        Options
      </div>
      <p className="mb-3 text-xs text-slate-500">
        Placeholder — real options for <code>{tool.id}</code> will be wired up
        when the tool is implemented.
      </p>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <label className="flex flex-col gap-1 text-xs">
          <span className="font-medium text-slate-700">Quality</span>
          <select
            value={(options.quality as string) ?? "balanced"}
            onChange={(e) => onChange({ ...options, quality: e.target.value })}
            className="h-9 rounded-lg border border-slate-200 px-2 text-sm"
          >
            <option value="low">Low</option>
            <option value="balanced">Balanced</option>
            <option value="high">High</option>
          </select>
        </label>
        <label className="flex flex-col gap-1 text-xs">
          <span className="font-medium text-slate-700">Custom note</span>
          <input
            type="text"
            placeholder="optional"
            value={(options.note as string) ?? ""}
            onChange={(e) => onChange({ ...options, note: e.target.value })}
            className="h-9 rounded-lg border border-slate-200 px-2 text-sm"
          />
        </label>
      </div>
    </div>
  );
}