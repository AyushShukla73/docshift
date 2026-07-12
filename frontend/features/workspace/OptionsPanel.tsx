"use client";

import { ToolDefinition } from "@/types/tool";
import PDFOrganizer from "@/components/preview/PDFOrganizer";
import EditingSession from "@/components/preview/EditingSession";
import { useState } from "react";
import { Icon } from "@/components/ui/Icon";

interface Props {
  tool: ToolDefinition | null;
  options: Record<string, unknown>;
  onChange: (next: Record<string, unknown>) => void;
  onRun: () => void;
}

export default function OptionsPanel({ tool, options, onChange }: Props) {
  const [selectedPages, setSelectedPages] = useState<number[]>([]);
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

      const previewPages = (options.previewPages as any) ?? [];

      const handleSelectionChange = (selected: number[]) => {
        setSelectedPages(selected);
        if (selected.length > 0) {
          onChange({
            ...options,
            selection_mode: "selected_pages",
            selected_pages: selected,
            range_start: Math.min(...selected),
            range_end: Math.max(...selected),
          });
        } else {
          const updated = { ...options };
          delete updated.selection_mode;
          delete updated.selected_pages;
          delete updated.range_start;
          delete updated.range_end;
          onChange(updated);
        }
      };

      if (tool.id === "split_pdf") {
      const validationError = options.mode === "range" && selectedPages.length === 0;

      return (
        <div className="rounded-xl border border-slate-200 bg-white p-4">
          <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
            Split options
          </div>
          <label className="flex flex-col gap-1 text-xs">
            <span className="font-medium text-slate-700">Mode</span>
            <select
              value={(options.mode as string) ?? "each"}
              onChange={(e) => {
                const newMode = e.target.value;
                const updated = { ...options, mode: newMode };
                if (newMode === "range") {
                  if (updated.range_start === undefined) updated.range_start = 1;
                  if (updated.range_end === undefined) updated.range_end = 1;
                }
                if (newMode === "n") {
                  if (updated.n_pages === undefined) updated.n_pages = 2;
                }
                onChange(updated);
              }}
              className="h-9 rounded-lg border border-slate-200 px-2 text-sm"
            >
              <option value="range">Page range</option>
              <option value="each">Each page separate</option>
              <option value="n">Every N pages</option>
            </select>
          </label>
          {options.mode === "range" && (
            <div className="mt-2">
              <PDFOrganizer
                data={previewPages}
                selectionMode={true}
                selectedPages={selectedPages}
                onSelectionChange={handleSelectionChange}
              />
              {validationError && (
                <p className="mt-1 text-xs text-red-600">Select at least one page.</p>
              )}
              <div className="mt-1 text-xs text-slate-600">
                Selected: {selectedPages.length ? selectedPages.join(", ") : "none"}
              </div>
            </div>
          )}
          {options.mode === "n" && (
            <label className="flex flex-col gap-1 text-xs mt-2">
              <span className="font-medium text-slate-700">Pages per split</span>
              <input
                type="number"
                min={1}
                value={(options.n_pages as number) ?? 2}
                onChange={(e) => onChange({ ...options, n_pages: Number(e.target.value) })}
                className="h-9 rounded-lg border border-slate-200 px-2 text-sm"
              />
            </label>
          )}
        </div>
      );
    }

  if (tool.id === "delete_pdf_pages") {
      const previewPages = (options.previewPages as any) ?? [];
      return (
        <EditingSession
          previewPages={previewPages}
          onRun={onRun}
          onChange={onChange}
        />
      );
    }
    if (tool.id === "pdf_to_image") {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-4">
        <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
          Output format
        </div>
        <select
          value={(options.format as string) ?? "png"}
          onChange={(e) => onChange({ ...options, format: e.target.value })}
          className="h-9 rounded-lg border border-slate-200 px-2 text-sm"
        >
          <option value="png">PNG</option>
          <option value="jpg">JPG</option>
        </select>
      </div>
    );
  }

  if (tool.id === "protect_pdf") {
    const pwd = (options.password as string) ?? "";
    const showError = pwd.trim().length === 0;
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-4">
        <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
          Protect options
        </div>
        <label className="flex flex-col gap-1 text-xs">
          <span className="font-medium text-slate-700">Password</span>
          <input
            type="password"
            placeholder="Enter password"
            value={pwd}
            onChange={(e) => onChange({ ...options, password: e.target.value })}
            className={`h-9 rounded-lg border ${showError ? "border-red-400" : "border-slate-200"} px-2 text-sm`}
          />
          {showError && (
            <p className="mt-1 text-xs text-red-600">Password required to protect PDF.</p>
          )}
        </label>
      </div>
    );
  }

  
      if (tool.id === "compress_pdf") {
        return (
          <div className="rounded-xl border border-slate-200 bg-white p-4">
            <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
              Compression level
            </div>
            <select
              value={(options.level as string) ?? "medium"}
              onChange={(e) => onChange({ ...options, level: e.target.value })}
              className="h-9 rounded-lg border border-slate-200 px-2 text-sm"
            >
              <option value="low">Low – best quality (larger file)</option>
              <option value="medium">Medium – balanced</option>
              <option value="high">High – strongest compression (smaller file)</option>
            </select>
          </div>
        );
      }

      if (tool.id === "unlock_pdf") {
    const pwd = (options.password as string) ?? "";
    const showError = pwd.trim().length === 0;
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-4">
        <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">
          Unlock options
        </div>
        <label className="flex flex-col gap-1 text-xs">
          <span className="font-medium text-slate-700">Password</span>
          <input
            type="password"
            placeholder="Enter password"
            value={pwd}
            onChange={(e) => onChange({ ...options, password: e.target.value })}
            className={`h-9 rounded-lg border ${showError ? "border-red-400" : "border-slate-200"} px-2 text-sm`}
          />
          {showError && (
            <p className="mt-1 text-xs text-red-600">Password required to unlock PDF.</p>
          )}
        </label>
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