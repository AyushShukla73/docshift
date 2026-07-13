// PageThumbnail component: displays a single PDF page thumbnail with page number.

import React from "react";
import Image from "next/image";

interface Props {
  src: string;
  page: number;
  alt?: string;
  selected?: boolean;
  onSelect?: () => void;
  draggable?: boolean;
  onDragStart?: (e: React.DragEvent<HTMLButtonElement>) => void;
  onDragOver?: (e: React.DragEvent<HTMLButtonElement>) => void;
  onDrop?: (e: React.DragEvent<HTMLButtonElement>) => void;
}

export default function PageThumbnail({ src, page, alt, selected = false, onSelect, draggable, onDragStart, onDragOver, onDrop }: Props) {
  const label = alt ?? `Page ${page}`;
  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onSelect?.();
    }
  };
  return (
    <button draggable={draggable} onDragStart={onDragStart} onDragOver={onDragOver} onDrop={onDrop}
      type="button"
      onClick={onSelect}
      onKeyDown={handleKey}
      className={`flex flex-col items-center focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 ${selected ? 'ring-2 ring-brand-500' : ''}`}
      aria-pressed={selected}
      aria-label={label}
    >
      <Image src={src} alt={label} width={160} height={210} className={`object-contain ${selected ? 'opacity-80' : ''}`} />
      <figcaption className="mt-1 text-sm font-medium text-gray-700 dark:text-gray-300">
        Page {page}
      </figcaption>
    </button>
  );
}
