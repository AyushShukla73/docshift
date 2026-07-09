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
}

export interface Job {
  job_id: string;
  status: string;
  tool_id: string;
  output?: JobOutput;
  error?: string | null;
}