"use client";

interface Props {
  data: string | { text: string };
}

export default function TextPreview({ data }: Props) {
  const text = typeof data === "string" ? data : data?.text ?? "";
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (e) {
      // ignore silently
    }
  };
  return (
    <div className="mt-4 rounded-xl border border-slate-200 bg-white p-4">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-slate-700">Preview</span>
        <button
          onClick={copyToClipboard}
          className="text-xs text-blue-600 hover:underline"
          aria-label="Copy preview text"
        >
          Copy
        </button>
      </div>
      <pre className="whitespace-pre-wrap text-sm text-slate-800 overflow-auto max-h-96">
        {text}
      </pre>
    </div>
  );
}
