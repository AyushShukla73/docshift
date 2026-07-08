import { NormalizedFileType } from "./file";

export type ToolCategory =
  | "convert"
  | "organize"
  | "optimize"
  | "extract";

export interface ToolDefinition {
  id: string;
  label: string;
  description: string;
  category: ToolCategory;
  supportedInputs: NormalizedFileType[];
  outputType: string;
  multiFile: boolean;
  configurable: boolean;
  /** Optional schema for the options panel, used later. */
  optionsSchema?: Record<string, unknown>;
}