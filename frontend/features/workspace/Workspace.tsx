"use client";

import { useCallback, useMemo, useState } from "react";
import SourcePanel from "./SourcePanel";
import ActionPanel from "./ActionPanel";
import { UploadedFile } from "@/types/file";
import { ToolDefinition } from "@/types/tool";
import { Job } from "@/types/job";
import { createJob } from "@/lib/api/jobs";
import { Card, CardBody } from "@/components/ui/Card";

export default function Workspace() {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [selectedToolId, setSelectedToolId] = useState<string | null>(null);
  const [options, setOptions] = useState<Record<string, unknown>>({});
  const [isProcessing, setIsProcessing] = useState(false);
  const [job, setJob] = useState<Job | null>(null);
  const [error, setError] = useState<string | null>(null);

  const detectedTypes = useMemo(
    () => Array.from(new Set(files.map((f) => f.detectedType))),
    [files]
  );

  const selectedTool: ToolDefinition | null = useMemo(() => {
    if (!selectedToolId) return null;
    // Look up via registry through the filter lib for safety.
    const { getToolById } = require("@/lib/toolFilter");
    return getToolById(selectedToolId) as ToolDefinition | null;
  }, [selectedToolId]);

  const handleFilesAdded = useCallback((next: UploadedFile[]) => {
    setFiles((prev) => {
      // Enforce multi-file vs single-file at the upload boundary for now.
      // Single-file tools replace; multi-file tools append.
      return [...prev, ...next];
    });
    setJob(null);
    setError(null);
  }, []);

  const handleRemoveFile = useCallback((id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id));
    setJob(null);
    setError(null);
  }, []);

  const handleReplace = useCallback((next: UploadedFile[]) => {
    setFiles(next);
    setJob(null);
    setError(null);
  }, []);

  const handleClearAll = useCallback(() => {
    setFiles([]);
    setSelectedToolId(null);
    setOptions({});
    setJob(null);
    setError(null);
  }, []);

  const canRun =
    files.length > 0 &&
    selectedTool !== null &&
    !isProcessing &&
    (selectedTool.multiFile ? files.length >= 1 : files.length === 1);

  const handleRun = useCallback(async () => {
    if (!selectedTool) return;
    setIsProcessing(true);
    setError(null);
    setJob(null);
    try {
      // Front‑end validation for tools that require extra options
      if (selectedTool?.id === "protect_pdf") {
        const pwd = (options.password as string) ?? "";
        if (!pwd.trim()) {
          setError("Password is required for Protect PDF");
          setIsProcessing(false);
          return;
        }
      }
      const result = await createJob({
        toolId: selectedTool.id,
        files: files.map((f) => f.file),
        options,
      });
      setJob(result);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Unexpected error";
      setError(msg);
    } finally {
      setIsProcessing(false);
    }
  }, [selectedTool, files, options]);

  return (
    <main className="min-h-screen w-full">
      <Header />

      <section className="mx-auto max-w-6xl px-4 pb-16 pt-4">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900">
            Workspace
          </h1>
          <p className="text-sm text-slate-500">
            Upload a document on the left, pick a tool on the right, and run it.
          </p>
        </div>

        <Card>
          <CardBody className="p-0">
            <div className="grid grid-cols-1 lg:grid-cols-2 lg:divide-x lg:divide-slate-100">
              <SourcePanel
                files={files}
                onAdd={handleFilesAdded}
                onRemove={handleRemoveFile}
                onReplace={handleReplace}
                onClearAll={handleClearAll}
                detectedTypes={detectedTypes}
              />
              <ActionPanel
                detectedTypes={detectedTypes}
                files={files}
                selectedTool={selectedTool}
                selectedToolId={selectedToolId}
                onSelectTool={setSelectedToolId}
                options={options}
                onOptionsChange={setOptions}
                onRun={handleRun}
                canRun={!!canRun}
                isProcessing={isProcessing}
                job={job}
                error={error}
              />
            </div>
          </CardBody>
        </Card>

        <p className="mt-6 text-center text-xs text-slate-400">
          DocShift foundation · tools are placeholders · build mode = scaffold
        </p>
      </section>
    </main>
  );
}

function Header() {
  return (
    <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="grid h-8 w-8 place-items-center rounded-lg bg-brand-600 text-white font-bold">
            D
          </div>
          <div>
            <div className="text-sm font-semibold leading-none">DocShift</div>
            <div className="text-[11px] text-slate-500 leading-none mt-0.5">
              Document workspace
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs text-slate-500">
          <span className="hidden sm:inline">v0.1.0 · foundation</span>
        </div>
      </div>
    </header>
  );
}