import { TOOL_REGISTRY } from "@/config/tools";
import { NormalizedFileType } from "@/types/file";
import { ToolDefinition } from "@/types/tool";

export function getCompatibleTools(
  types: NormalizedFileType[]
): ToolDefinition[] {
  if (types.length === 0) return [];
  return TOOL_REGISTRY.filter((tool) =>
    types.some((t) => tool.supportedInputs.includes(t))
  );
}

export function getToolById(toolId: string | null) {
  if (!toolId) return null;
  return TOOL_REGISTRY.find((t) => t.id === toolId) ?? null;
}