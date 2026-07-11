"use client";

interface Props {
  data: string | { src: string; alt?: string };
}

export default function PdfThumbnailPreview({ data }: Props) {
  const src = typeof data === "string" ? data : data?.src;
  const alt = typeof data === "string" ? "" : data?.alt ?? "PDF thumbnail";
  const [open, setOpen] = React.useState(false);
  if (!src) return null;
  const openModal = () => setOpen(true);
  const closeModal = () => setOpen(false);
  return (
    <>
      <div className="mt-4 flex justify-center">
        <img
          src={src}
          alt={alt}
          className="max-w-full max-h-96 rounded cursor-pointer"
          onClick={openModal}
          aria-label="Open PDF thumbnail"
        />
      </div>
      {open && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75"
          onClick={closeModal}
          role="dialog"
          aria-modal="true"
        >
          <img src={src} alt={alt} className="max-w-full max-h-full" />
        </div>
      )}
    </>
  );
}
