export type JobStatus = "pending" | "processing" | "completed" | "failed";

export interface JobInput {
  file_id: string;
  filename: string;
  detected_type: string;
  size_bytes: number;
}

export interface JobOutput {
  filename?: string;
  download_url?: string;
  size_bytes?: number;
}

export interface Job {
  job_id: string;
  tool_id: string;
  status: JobStatus;
  created_at: string;
  updated_at: string;
  inputs: JobInput[];
  options: Record<string, unknown>;
  output: JobOutput | null;
  error: string | null;
}