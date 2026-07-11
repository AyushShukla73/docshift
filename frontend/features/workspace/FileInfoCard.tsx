"use client";

import { ChangeEvent, useRef } from "react";
import { UploadedFile } from "@/types/file";
import { Badge } from "@/components/ui/Badge";
import { Icon } from "@/components/ui/Icon";
import { humanSize } from "@/lib/utils";
import { toUploadedFile } from "@/lib/fileDetection";

interface Props {
  file: UploadedFile;
  onRemove: () => void;
  onReplace: (files: UploadedFile[]) => void;
  isProcessing: boolean;
}

export default function FileInfoCard({ file, onRemove, onReplace, isProcessing }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleReplace = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) onReplace([toUploadedFile(f)]);
    e.target.value = "";
  };

  return (
    <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3">
      <div className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-brand-50 text-brand-700">
        <Icon name="file" className="h-5 w-5" />
      </div>

      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <p className="truncate text-sm font-medium text-slate-900">
            {file.name}
          </p>
          <Badge tone="brand">{file.detectedType}</Badge>
        </div>
        <p className="mt-0.5 text-xs text-slate-500">
          {file.detectedLabel} · {humanSize(file.sizeBytes)}
        </p>
      </div>

      <div className="flex items-center gap-1">
        <button
          onClick={() => inputRef.current?.click()}
          className="rounded-lg px-2 py-1 text-xs font-medium text-slate-600 hover:bg-slate-100"
          title="Replace file"
          disabled={isProcessing}
        >
          Replace
        </button>
        <button
          onClick={onRemove}
          className="grid h-8 w-8 place-items-center rounded-lg text-slate-500 hover:bg-red-50 hover:text-red-600"
          title="Remove file"
          disabled={isProcessing}
        >
          <Icon name="trash" className="h-4 w-4" />
        </button>
        <input
          ref={inputRef}
          type="file"
          className="hidden"
          onChange={handleReplace}
        />
      </div>
    </div>
  );
}