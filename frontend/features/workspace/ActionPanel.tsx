"use client";

import { useMemo } from "react";
import { NormalizedFileType } from "@/types/file";
import { ToolDefinition } from "@/types/tool";
import { Job } from "@/types/job";
import CategorySelector from "./CategorySelector";
import ToolSelector from "./ToolSelector";
import OptionsPanel from "./OptionsPanel";
import ActionFooter from "./ActionFooter";
import ResultCard from "./ResultCard";
import { getCompatibleTools } from "@/lib/toolFilter";
import { CATEGORY_ORDER } from "@/config/categories";

interface Props {
  detectedTypes: NormalizedFileType[];
  files: { id: string }[];
  selectedTool: ToolDefinition | null;
  selectedToolId: string | null;
  onSelectTool: (id: string | null) => void;
  options: Record<string, unknown>;
  onOptionsChange: (next: Record<string, unknown>) => void;
  onRun: () => void;
  canRun: boolean;
  isProcessing: boolean;
  job: Job | null;
  error: string | null;
}

export default function ActionPanel({
  detectedTypes,
  files,
  selectedTool,
  selectedToolId,
  onSelectTool,
  options,
  onOptionsChange,
  onRun,
  canRun,
  isProcessing,
  job,
  error,
}: Props) {
  const compatibleTools = useMemo(
    () => getCompatibleTools(detectedTypes),
    [detectedTypes]
  );

  const hasFiles = files.length > 0;

  return (
    <div className="flex flex-col p-5 lg:p-6 min-h-[520px]">
      <div className="mb-4">
        <h2 className="text-sm font-semibold text-slate-900">Tools</h2>
        <p className="text-xs text-slate-500">
          {hasFiles
            ? "Compatible with your uploaded file(s)"
            : "Upload a file to see available tools"}
        </p>
      </div>

      {!hasFiles ? (
        <EmptyToolsState />
      ) : compatibleTools.length === 0 ? (
        <NoCompatibleToolsState types={detectedTypes} />
      ) : (
        <div className="flex flex-1 flex-col gap-4">
          <CategorySelector
            tools={compatibleTools}
            selectedToolId={selectedToolId}
            onSelect={onSelectTool}
          />
          <ToolSelector
            tools={compatibleTools}
            selectedToolId={selectedToolId}
            onSelect={onSelectTool}
            categories={CATEGORY_ORDER}
          />
          <OptionsPanel tool={selectedTool} options={options} onChange={onOptionsChange} />
          <ResultCard job={job} error={error} isProcessing={isProcessing} />
          <div className="mt-auto">
            <ActionFooter
              tool={selectedTool}
              canRun={canRun}
              isProcessing={isProcessing}
              onRun={onRun}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function EmptyToolsState() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center rounded-2xl border border-dashed border-slate-200 p-10 text-center">
      <div className="mb-3 grid h-12 w-12 place-items-center rounded-xl bg-slate-100 text-slate-400">
        <Icon name="swap" />
      </div>
      <p className="text-sm font-medium text-slate-700">No file yet</p>
      <p className="mt-1 text-xs text-slate-500">
        Tools will appear here once a file is uploaded on the left.
      </p>
    </div>
  );
}

function NoCompatibleToolsState({ types }: { types: string[] }) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center rounded-2xl border border-amber-200 bg-amber-50 p-10 text-center">
      <p className="text-sm font-medium text-amber-800">
        No tools available for {types.join(", ")}
      </p>
      <p className="mt-1 text-xs text-amber-700">
        Try uploading a PDF, DOCX, JPG, PNG, or WEBP file.
      </p>
    </div>
  );
}

import { Icon } from "@/components/ui/Icon";