"use client";

import { ToolDefinition } from "@/types/tool";
import { Button } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";

interface Props {
  tool: ToolDefinition | null;
  canRun: boolean;
  isProcessing: boolean;
  onRun: () => void;
}

export default function ActionFooter({
  tool,
  canRun,
  isProcessing,
  onRun,
}: Props) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50/60 p-3">
      <div className="min-w-0">
        <p className="text-xs font-medium text-slate-700">
          {tool ? tool.label : "No tool selected"}
        </p>
        <p className="truncate text-[11px] text-slate-500">
          {tool
            ? `Output: ${tool.outputType}${tool.multiFile ? " · multi-file" : ""}`
            : "Pick a tool above to continue"}
        </p>
      </div>
      <Button
        onClick={onRun}
        disabled={!canRun}
        loading={isProcessing}
        size="lg"
      >
        {!isProcessing && <Icon name="arrowRight" className="h-4 w-4" />}
        {isProcessing ? "Processing…" : "Run tool"}
      </Button>
    </div>
  );
}