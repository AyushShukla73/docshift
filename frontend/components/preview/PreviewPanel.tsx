"use client";

import { JobOutput } from "@/types/job";
import TextPreview from "./TextPreview";
import ImagePreview from "./ImagePreview";
import ImageGalleryPreview from "./ImageGalleryPreview";
import PdfThumbnailPreview from "./PdfThumbnailPreview";
import GenericPreview from "./GenericPreview";

interface Props {
  preview?: JobOutput["preview"];
}

export default function PreviewPanel({ preview }: Props) {
  if (!preview) return null;

  switch (preview.type) {
    case "text":
      return <TextPreview data={preview.data} />;
    case "image":
      return <ImagePreview data={preview.data} />;
    case "image_gallery":
      return <ImageGalleryPreview data={preview.data} />;
    case "pdf_thumbnail":
      return <PdfThumbnailPreview data={preview.data} />;
    default:
      return <GenericPreview data={preview.data} />;
  }
}
