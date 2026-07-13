// PDFOrganizer component: reusable page‑management workspace.

import React from "react";
import PageGrid from "./PageGrid";

interface PageData {
  src: string;
  page: number;
}

interface Props {
  selectionMode?: boolean;
  onUndo?: () => void;
  onRedo?: () => void;
  onApply?: () => void;
  onCancel?: () => void;
  canUndo?: boolean;
  canRedo?: boolean;
  dirty?: boolean;
  onReorder?: (newData: PageData[]) => void;

  data: PageData[];
  selectedPages: number[];
  onSelectionChange: (pages: number[]) => void;
  onDelete?: () => void;
}

export default function PDFOrganizer({ data, selectedPages, onSelectionChange, onDelete, onUndo, onRedo, onApply, onCancel, onReorder, canUndo, canRedo, dirty, selectionMode }: Props) {
  const total = data.length;
  const selectAll = () => onSelectionChange(data.map(p => p.page));
  const clear = () => onSelectionChange([]);

  if (total === 0) {
    return (
      <div className="p-4 text-center text-sm text-slate-500">
        No pages available.
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      <div className="flex items-center justify-between p-2 border-b border-slate-200">
        <div className="text-xs text-slate-600">
          Total pages: {total} • Selected: {selectedPages.length}
        </div>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={selectAll}
            className="px-2 py-1 text-xs text-white bg-brand-600 rounded hover:bg-brand-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-500"
          >
            Select All
          </button>
          <button
            type="button"
            onClick={clear}
            className="px-2 py-1 text-xs text-white bg-gray-600 rounded hover:bg-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500"
          >
            Clear
          </button>
          {onDelete && (
                <button
                  type="button"
                  onClick={onDelete}
                  className="px-2 py-1 text-xs text-white bg-red-600 rounded hover:bg-red-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-red-500"
                >
                  Delete Selected
                </button>
              )}
              {onUndo && (
                <button
                  type="button"
                  onClick={onUndo}
                  disabled={!canUndo}
                  className="px-2 py-1 text-xs text-white bg-gray-500 rounded hover:bg-gray-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-400"
                >
                  Undo
                </button>
              )}
              {onRedo && (
                <button
                  type="button"
                  onClick={onRedo}
                  disabled={!canRedo}
                  className="px-2 py-1 text-xs text-white bg-gray-500 rounded hover:bg-gray-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-400"
                >
                  Redo
                </button>
              )}
              {onApply && (
                <button
                  type="button"
                  onClick={onApply}
                  disabled={!dirty}
                  className="px-2 py-1 text-xs text-white bg-green-600 rounded hover:bg-green-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-green-500"
                >
                  Apply Changes
                </button>
              )}
              {onCancel && (
                <button
                  type="button"
                  onClick={onCancel}
                  disabled={!dirty}
                  className="px-2 py-1 text-xs text-white bg-gray-600 rounded hover:bg-gray-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500"
                >
                  Cancel Editing
                </button>
              )}
        </div>
      </div>
      <PageGrid
        data={data}
        selectionMode={true}
        selectedPages={selectedPages}
        onSelectionChange={onSelectionChange}
        onReorder={onReorder}
      />
    </div>
  );
}
