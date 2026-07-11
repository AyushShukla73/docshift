// PageGrid component: responsive grid of PDF page thumbnails.

import PageThumbnail from "./PageThumbnail";

interface PageData {
  src: string;
  page: number;
}

interface Props {
  data: PageData[];
  selectionMode?: boolean;
  selectedPages?: number[];
  onSelectionChange?: (selected: number[]) => void;
}

export default function PageGrid({ data, selectionMode = false, selectedPages = [], onSelectionChange }: Props) {
  const selectedSet = new Set(selectedPages);
  const togglePage = (page: number) => {
    if (!onSelectionChange) return;
    const newSelected = new Set(selectedSet);
    if (newSelected.has(page)) {
      newSelected.delete(page);
    } else {
      newSelected.add(page);
    }
    onSelectionChange(Array.from(newSelected).sort((a,b)=>a-b));
  };

  return (
    <div className="mt-4 grid gap-4" style={{
      gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))",
    }}>
      {data.map((p) => (
        <PageThumbnail
          key={p.page}
          src={p.src}
          page={p.page}
          selected={selectionMode && selectedSet.has(p.page)}
          onSelect={() => selectionMode && togglePage(p.page)}
        />
      ))}
    </div>
  );
}
