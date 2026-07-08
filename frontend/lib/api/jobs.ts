import { Job } from "@/types/job";
import { apiFetch } from "./client";

export interface CreateJobArgs {
  toolId: string;
  files: File[];
  options?: Record<string, unknown>;
}

export async function createJob(args: CreateJobArgs): Promise<Job> {
  const form = new FormData();
  form.append("tool_id", args.toolId);
  if (args.options) {
    form.append("options", JSON.stringify(args.options));
  }
  for (const f of args.files) {
    form.append("files", f, f.name);
  }

  return apiFetch<Job>("/api/jobs/request", {
    method: "POST",
    body: form,
  });
}

export async function getJob(jobId: string): Promise<Job> {
  return apiFetch<Job>(`/api/jobs/${jobId}`);
}