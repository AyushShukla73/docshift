// PageThumbnail component: displays a single PDF page thumbnail with page number.

import Image from "next/image";

interface Props {
  src: string;
  page: number;
  alt?: string;
}

export default function PageThumbnail({ src, page, alt }: Props) {
  const label = alt ?? `Page ${page}`;
  return (
    <figure className="flex flex-col items-center">
      <Image src={src} alt={label} width={160} height={210} className="object-contain" />
      <figcaption className="mt-1 text-sm font-medium text-gray-700 dark:text-gray-300">
        Page {page}
      </figcaption>
    </figure>
  );
}
