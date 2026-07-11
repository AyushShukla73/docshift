"use client";

interface Props {
  data: string | { src: string; alt?: string };
}

export default function PdfThumbnailPreview({ data }: Props) {
  const src = typeof data === "string" ? data : data?.src;
  const alt = typeof data === "string" ? "" : data?.alt ?? "PDF thumbnail";
  if (!src) return null;
  return (
    <div className="mt-4 flex justify-center">
      <img src={src} alt={alt} className="max-w-full rounded" />
    </div>
  );
}
