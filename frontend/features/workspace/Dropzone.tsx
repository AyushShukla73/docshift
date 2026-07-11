"use client";

import { ChangeEvent, DragEvent, useRef, useState } from "react";
import { UploadedFile } from "@/types/file";
import {
  ACCEPTED_EXTENSIONS,
  isAcceptedFile,
  toUploadedFile,
} from "@/lib/fileDetection";
import { Icon } from "@/components/ui/Icon";
import { cn } from "@/lib/utils";

interface Props {
  onAdd: (files: UploadedFile[]) => void;
  disabled?: boolean;
}

export default function Dropzone({ onAdd, disabled }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [rejected, setRejected] = useState<string[]>([]);

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;
    const all = Array.from(fileList);
    const accepted = all.filter(isAcceptedFile);
    const denied = all.filter((f) => !isAcceptedFile(f)).map((f) => f.name);
    setRejected(denied);
    if (accepted.length > 0) {
      onAdd(accepted.map(toUploadedFile));
    }
  };

  const onDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;
    handleFiles(e.dataTransfer.files);
  };

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (disabled) return;
    handleFiles(e.target.files);
    e.target.value = "";
  };

  return (
    <div className="flex flex-1 flex-col">
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        className={cn(
          "group relative flex flex-1 flex-col items-center justify-center rounded-2xl border-2 border-dashed px-6 py-12 text-center transition-colors",
          isDragging ? "border-brand-400 bg-brand-50" : "border-slate-200",
          disabled && "cursor-not-allowed opacity-50"
        )}
      >
        <div
          className={cn(
            "mb-4 grid h-14 w-14 place-items-center rounded-2xl transition-colors",
            isDragging ? "bg-brand-100 text-brand-700" : "bg-slate-100 text-slate-600"
          )}
        >
          <Icon name="upload" className="h-6 w-6" />
        </div>
        <p className="text-sm font-medium text-slate-800">
          Drag & drop a file here
        </p>
        <p className="mt-1 text-xs text-slate-500">
          or click to browse from your computer
        </p>
        <p className="mt-4 text-[11px] uppercase tracking-wide text-slate-400">
          Supported: {ACCEPTED_EXTENSIONS.join(", ")}
        </p>

        <input
          ref={inputRef}
          type="file"
          multiple
          className="hidden"
          onChange={onChange}
        />
      </div>

      {rejected.length > 0 && (
        <div className="mt-3 rounded-lg bg-red-50 px-3 py-2 text-xs text-red-700">
          Skipped unsupported: {rejected.join(", ")}
        </div>
      )}
    </div>
  );
}