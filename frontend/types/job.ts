export type JobStatus = "pending" | "processing" | "completed" | "failed";

export interface JobInput {
  file_id: string;
  filename: string;
  detected_type: string;
  size_bytes: number;
}

export interface JobOutput {
  filename?: string;
  size_bytes?: number;
  mime_type?: string;
  download_url?: string;
  preview?: JobPreview;
}

export interface JobPreview {
  /** preview type, e.g. "text", "image", "image_gallery", "pdf_thumbnail", "generic" */
  type: string;
  /** arbitrary data for the specific preview component */
  data: any;
}

export interface Job {
  job_id: string;
  tool_id: string;
  status: "pending" | "processing" | "completed" | "failed";
  created_at?: string;
  updated_at?: string;
  inputs?: any[]; // keep generic, not used directly in UI
  options?: Record<string, unknown>;
  output?: JobOutput;
  error?: any; // can be string or object from backend
}