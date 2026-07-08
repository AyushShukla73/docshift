import { SVGProps } from "react";

const PATHS: Record<string, string> = {
  upload: "M12 16V4m0 0L8 8m4-4l4 4M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2",
  file: "M14 3v4a1 1 0 001 1h4M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V8l-6-5z",
  trash: "M6 7h12M9 7V5a1 1 0 011-1h4a1 1 0 011 1v2M6 7l1 12a2 2 0 002 2h6a2 2 0 002-2l1-12",
  swap: "M7 16V4m0 0L3 8m4-4l4 4M17 8v12m0 0l4-4m-4 4l-4-4",
  layers: "M12 3l9 5-9 5-9-5 9-5zM3 13l9 5 9-5",
  sparkles:
    "M5 3v4M3 5h4M19 13v4m-2-2h4M12 4l1.6 4.4L18 10l-4.4 1.6L12 16l-1.6-4.4L6 10l4.4-1.6L12 4z",
  scan: "M4 4h4M16 4h4M4 20h4M16 20h4M4 4v4M20 4v4M4 16v4M20 16v4M8 12h8",
  check: "M5 13l4 4L19 7",
  download: "M12 4v12m0 0l-4-4m4 4l4-4M4 20h16",
  arrowRight: "M5 12h14m0 0l-6-6m6 6l-6 6",
};

export function Icon({
  name,
  ...rest
}: SVGProps<SVGSVGElement> & { name: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.75}
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-5 w-5"
      {...rest}
    >
      <path d={PATHS[name] ?? ""} />
    </svg>
  );
}