"use client";
import React from "react";

import { Job } from "@/types/job";
import { getToolById } from "@/lib/toolFilter";
import { humanSize } from "@/lib/utils";
import { Badge } from "@/components/ui/Badge";
import { normalizeWarnings, extractErrorMessage, formatResultMeta } from "./resultHelpers";
import { Button } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";
import PreviewPanel from "@/components/preview/PreviewPanel";

interface Props {
  job: Job | null;
  error: string | null;
  isProcessing: boolean;
}

export default function ResultCard({ job, error, isProcessing }: Props) {
    const tool = job?.tool_id ? getToolById(job.tool_id) : null;
  const toolLabel = tool?.label ?? job?.tool_id ?? "";
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
    const isPlaceholder = /not yet implemented/.test(error);
    return (
      <div className={`rounded-xl border ${isPlaceholder ? 'border-amber-200 bg-amber-50' : 'border-red-200 bg-red-50'} p-4`}>
        <div className={`flex items-center gap-2 text-sm font-medium ${isPlaceholder ? 'text-amber-800' : 'text-red-800'}`}>
          <Icon name={isPlaceholder ? 'alertTriangle' : 'trash'} className="h-4 w-4" />
          {isPlaceholder ? 'Feature not available' : 'Something went wrong'}
        </div>
        <p className={`mt-1 text-xs ${isPlaceholder ? 'text-amber-700' : 'text-red-700'}`}>
          {isPlaceholder ? "This tool is a placeholder and isn’t implemented yet. Please try another tool or check back later." : error}
        </p>
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
            onClick={() => {
              const apiBase =
                process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

              let downloadUrl = job.output?.download_url?.trim();

              if (!downloadUrl) {
                downloadUrl = `${apiBase}/api/jobs/${job.job_id}/download`;
              } else if (downloadUrl.startsWith("/")) {
                downloadUrl = `${apiBase}${downloadUrl}`;
              } else if (
                !downloadUrl.startsWith("http://") &&
                !downloadUrl.startsWith("https://")
              ) {
                downloadUrl = `${apiBase}/${downloadUrl.replace(/^\/+/, "")}`;
              }

              window.open(downloadUrl, "_blank");
            }}
          >
            <Icon name="download" className="h-4 w-4" />
            Download
          </Button>
        </div>
      )}

      {ok && job.output?.preview && (
  <PreviewPanel preview={job.output.preview} />
)}
{ok && ((job.output as any)?.warnings?.length ?? 0) > 0 && (
        <div className="mt-2 space-y-1">
          {normalizeWarnings(job.output.warnings).map((w, i) => (
            <div key={i} className="flex items-start gap-1 text-xs text-yellow-700">
              <Icon name="alertTriangle" className="h-4 w-4 flex-shrink-0" />
              <span>{w}</span>
            </div>
          ))}
        </div>
      )}

            {ok && job.output?.output_files?.length > 1 && (
        <div className="mt-4">
          <div className="text-xs font-medium text-slate-700 mb-1">Generated files</div>
          <ul className="space-y-2">
            {job.output.output_files
              .filter((f) => f.name !== job.output?.filename)
              .map((f, idx) => (
                <li key={idx} className="flex items-center justify-between rounded bg-white p-2 text-sm">
                  <div className="min-w-0">
                    <p className="truncate font-medium text-slate-900">{f.name}</p>
                    <p className="text-[11px] text-slate-500">
                      {f.size_bytes ? humanSize(f.size_bytes) : "size unknown"} · {f.media_type ?? "unknown"}
                    </p>
                  </div>
                </li>
              ))}
          </ul>
        </div>
      )}

            {ok && job.output?.result_meta && formatResultMeta(job.output.result_meta).length > 0 && (
        <div className="mt-2">
          <div className="text-xs font-medium text-slate-700 mb-1">Details</div>
          <dl className="grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-slate-600">
            {formatResultMeta(job.output.result_meta).map(({ label, value }, i) => (
              <React.Fragment key={i}>
                <dt className="capitalize text-slate-500">{label}</dt>
                <dd>{value}</dd>
              </React.Fragment>
            ))}
          </dl>
        </div>
      )}

      {job.error && (
        <p className="mt-2 text-xs text-red-700">{extractErrorMessage(job.error)}</p>
      )}
    </div>
  );
}