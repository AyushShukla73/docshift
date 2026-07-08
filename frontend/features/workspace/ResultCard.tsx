"use client";

import { Job } from "@/types/job";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";
import { humanSize } from "@/lib/utils";

interface Props {
  job: Job | null;
  error: string | null;
  isProcessing: boolean;
}

export default function ResultCard({ job, error, isProcessing }: Props) {
  if (isProcessing) {
    return (
      <div className="rounded-xl border border-brand-200 bg-brand-50 p-4">
        <div className="flex items-center gap-2 text-sm text-brand-800">
          <span className="h-3 w-3 animate-spin rounded-full border-2 border-brand-400 border-t-brand-700" />
          Processing your file(s)…
        </div>
        <p className="mt-1 text-xs text-brand-700">
          The backend is running the tool placeholder.
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border border-red-200 bg-red-50 p-4">
        <div className="flex items-center gap-2 text-sm font-medium text-red-800">
          <Icon name="trash" className="h-4 w-4" />
          Something went wrong
        </div>
        <p className="mt-1 text-xs text-red-700">{error}</p>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="rounded-xl border border-dashed border-slate-200 bg-white p-4 text-center text-xs text-slate-500">
        Result will appear here after you run a tool.
      </div>
    );
  }

  const ok = job.status === "completed";

  return (
    <div
      className={`rounded-xl border p-4 ${
        ok ? "border-emerald-200 bg-emerald-50" : "border-amber-200 bg-amber-50"
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon
            name={ok ? "check" : "scan"}
            className={`h-4 w-4 ${ok ? "text-emerald-700" : "text-amber-700"}`}
          />
          <span
            className={`text-sm font-medium ${
              ok ? "text-emerald-900" : "text-amber-900"
            }`}
          >
            {ok ? "Done" : "Job status: " + job.status}
          </span>
        </div>
        <Badge tone={ok ? "success" : "warning"}>{job.status}</Badge>
      </div>

      {ok && job.output?.filename && (
        <div className="mt-3 flex items-center justify-between rounded-lg bg-white px-3 py-2">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-slate-900">
              {job.output.filename}
            </p>
            <p className="text-[11px] text-slate-500">
              {job.output.size_bytes
                ? humanSize(job.output.size_bytes)
                : "size unknown"}{" "}
              · job {job.job_id}
            </p>
          </div>
          <Button
            size="sm"
            variant="secondary"
            onClick={() =>
              alert(
                `Placeholder download for ${job.output?.filename}.\nWire this to /api/jobs/${job.job_id}/download when real output exists.`
              )
            }
          >
            <Icon name="download" className="h-4 w-4" />
            Download
          </Button>
        </div>
      )}

      {job.error && (
        <p className="mt-2 text-xs text-red-700">{job.error}</p>
      )}
    </div>
  );
}