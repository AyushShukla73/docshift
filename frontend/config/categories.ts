import { ToolCategory } from "@/types/tool";

export const CATEGORY_META: Record<
  ToolCategory,
  { label: string; description: string; icon: string }
> = {
  convert: {
    label: "Convert",
    description: "Change file format",
    icon: "swap",
  },
  organize: {
    label: "Organize",
    description: "Merge, split & arrange",
    icon: "layers",
  },
  optimize: {
    label: "Optimize",
    description: "Compress & clean up",
    icon: "sparkles",
  },
  extract: {
    label: "Extract",
    description: "Pull content out",
    icon: "scan",
  },
};

export const CATEGORY_ORDER: ToolCategory[] = [
  "convert",
  "organize",
  "optimize",
  "extract",
];