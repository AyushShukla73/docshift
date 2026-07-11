"use client";

interface Props {
  data: string | { text: string };
}

export default function TextPreview({ data }: Props) {
  const text = typeof data === "string" ? data : data?.text ?? "";
  return (
    <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4">
      <pre className="whitespace-pre-wrap text-sm text-slate-800">{text}</pre>
    </div>
  );
}
