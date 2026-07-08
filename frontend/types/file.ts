export type NormalizedFileType =
  | "pdf"
  | "docx"
  | "doc"
  | "jpg"
  | "png"
  | "webp"
  | "gif"
  | "txt"
  | "unknown";

export interface UploadedFile {
  id: string;          // local id
  file: File;
  name: string;
  sizeBytes: number;
  detectedType: NormalizedFileType;
  detectedLabel: string;
}