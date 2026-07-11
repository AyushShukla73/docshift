"use client";

interface Props {
  data: any;
}

export default function GenericPreview({ data }: Props) {
  return (
    <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4 text-center text-sm text-slate-600">
      Preview unavailable – this file type does not currently support visual preview.
    </div>
  );
}
