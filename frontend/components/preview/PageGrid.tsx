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
  return (
    <div className="mt-4 grid gap-4" style={{
      gridTemplateColumns: "repeat(auto-fill, minmax(120px, 1fr))",
    }}>
      {data.map((p) => (
        <PageThumbnail key={p.page} src={p.src} page={p.page} />
      ))}
    </div>
  );
}
