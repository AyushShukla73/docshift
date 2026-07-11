"use client";

interface Props {
  data: string[] | { images: string[] };
}

export default function ImageGalleryPreview({ data }: Props) {
  let images: string[] = [];
  if (Array.isArray(data)) images = data;
  else if (data && Array.isArray((data as any).images)) images = (data as any).images;
  if (images.length === 0) return null;
  return (
    <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4">
      {images.map((src, i) => (
        <img key={i} src={src} alt={`Preview ${i + 1}`} className="rounded" />
      ))}
    </div>
  );
}
