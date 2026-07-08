import { NormalizedFileType, UploadedFile } from "@/types/file";
import { uid } from "./utils";

const EXT_MAP: Record<string, NormalizedFileType> = {
  pdf: "pdf",
  docx: "docx",
  doc: "doc",
  jpg: "jpg",
  jpeg: "jpg",
  png: "png",
  webp: "webp",
  gif: "gif",
  txt: "txt",
};

const TYPE_LABELS: Record<string, string> = {
  pdf: "PDF Document",
  docx: "Word Document",
  doc: "Word Document (legacy)",
  jpg: "JPEG Image",
  png: "PNG Image",
  webp: "WebP Image",
  gif: "GIF Image",
  txt: "Plain Text",
  unknown: "Unknown",
};

export const ACCEPTED_EXTENSIONS = Object.keys(EXT_MAP);

export function detectFileType(file: File): NormalizedFileType {
  const name = file.name.toLowerCase();
  if (name.includes(".")) {
    const ext = name.split(".").pop()!;
    if (ext in EXT_MAP) return EXT_MAP[ext];
  }
  // Fall back to MIME sniffing.
  if (file.type === "application/pdf") return "pdf";
  if (file.type === "application/msword") return "doc";
  if (
    file.type ===
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
  )
    return "docx";
  if (file.type === "image/jpeg") return "jpg";
  if (file.type === "image/png") return "png";
  if (file.type === "image/webp") return "webp";
  if (file.type === "image/gif") return "gif";
  if (file.type === "text/plain") return "txt";
  return "unknown";
}

export function typeLabel(t: NormalizedFileType): string {
  return TYPE_LABELS[t] ?? "Unknown";
}

export function isAcceptedFile(file: File): boolean {
  return detectFileType(file) !== "unknown";
}

export function toUploadedFile(file: File): UploadedFile {
  const detectedType = detectFileType(file);
  return {
    id: uid("file"),
    file,
    name: file.name,
    sizeBytes: file.size,
    detectedType,
    detectedLabel: typeLabel(detectedType),
  };
}