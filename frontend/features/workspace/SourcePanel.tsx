"use client";

import { useMemo } from "react";
import Dropzone from "./Dropzone";
import FileInfoCard from "./FileInfoCard";
import { UploadedFile } from "@/types/file";
import { NormalizedFileType } from "@/types/file";
import { Badge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";
import { Button } from "@/components/ui/Button";

interface Props {
  files: UploadedFile[];
  detectedTypes: NormalizedFileType[];
  onAdd: (files: UploadedFile[]) => void;
  onRemove: (id: string) => void;
  onReplace: (files: UploadedFile[]) => void;
  onClearAll: () => void;
  duplicateNames?: string[];
  isProcessing: boolean;
}

export default function SourcePanel({
  files,
  detectedTypes,
  onAdd,
  onRemove,
  onReplace,
  onClearAll,
  duplicateNames,
  isProcessing,
}: Props) {
  const isEmpty = files.length === 0;

  const totalSize = useMemo(
    () => files.reduce((sum, f) => sum + f.sizeBytes, 0),
    [files]
  );

  return (
    <div className="flex flex-col p-5 lg:p-6 min-h-[520px]">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-sm font-semibold text-slate-900">Source</h2>
          <p className="text-xs text-slate-500">
            Drop a file to get started
          </p>
        </div>
        {files.length > 0 && (
          <div className="flex items-center gap-2">
            <Badge tone="brand">{files.length} file(s)</Badge>
            <Button size="sm" variant="ghost" onClick={onClearAll} disabled={isProcessing}>
              Clear all
            </Button>
          </div>
        )}
      </div>

      {isEmpty ? (
        <>
          <Dropzone onAdd={onAdd} disabled={isProcessing} />
          {duplicateNames && duplicateNames.length > 0 && (
            <div className="mt-2 rounded-lg bg-yellow-50 px-3 py-2 text-xs text-yellow-700">
              Duplicate files ignored: {duplicateNames.join(", ")}
            </div>
          )}
        </>
      ) : (
        <div className="flex flex-col gap-3">
          {files.map((f) => (
            <FileInfoCard
              key={f.id}
              file={f}
              onRemove={() => onRemove(f.id)}
              onReplace={onReplace}
            />
          ))}

          <div className="mt-2 rounded-xl border border-dashed border-slate-200 p-3 text-center">
            <p className="text-xs text-slate-500">
              Add more files for multi-file tools (e.g. Merge PDFs).
            </p>
            <AddMoreButton onAdd={onAdd} />
          </div>

          <div className="mt-2 flex flex-wrap items-center gap-2">
            <span className="text-xs text-slate-400">Detected types:</span>
            {detectedTypes.map((t) => (
              <Badge key={t} tone="neutral">
                {t}
              </Badge>
            ))}
            <span className="ml-auto text-xs text-slate-400">
              total {(totalSize / 1024 / 1024).toFixed(2)} MB
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

function AddMoreButton({ onAdd }: { onAdd: (f: UploadedFile[]) => void }) {
  return (
    <label className="mt-2 inline-flex cursor-pointer items-center gap-1 text-xs font-medium text-brand-700 hover:text-brand-800">
      <Icon name="upload" className="h-3.5 w-3.5" />
      Add files
      <input
        type="file"
        multiple
        className="hidden"
        onChange={(e) => {
          const fs = Array.from(e.target.files ?? []);
          import("@/lib/fileDetection").then(({ toUploadedFile }) => {
            onAdd(fs.map(toUploadedFile));
          });
        }}
      />
    </label>
  );
}