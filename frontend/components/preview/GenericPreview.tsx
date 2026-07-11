"use client";

interface Props {
  data: any;
}

export default function GenericPreview({ data }: Props) {
  // Fallback: render JSON of data
  try {
    const txt = typeof data === "string" ? data : JSON.stringify(data, null, 2);
    return (
      <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4">
        <pre className="whitespace-pre-wrap text-sm text-slate-800">{txt}</pre>
      </div>
    );
  } catch {
    return null;
  }
}
