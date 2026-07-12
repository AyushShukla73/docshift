"use client";

import React, { useState, useEffect } from "react";
import PDFOrganizer from "./PDFOrganizer";

interface Props {
  previewPages: any[]; // PageData[] shape
  onRun: () => void;
  onChange: (next: Record<string, unknown>) => void;
}

export default function EditingSession({ previewPages, onRun, onChange }: Props) {
  const [pages, setPages] = useState(previewPages);
  const [selected, setSelected] = useState<number[]>([]);
  const [undoStack, setUndoStack] = useState<any[]>([]);
  const [redoStack, setRedoStack] = useState<any[]>([]);
  const [pendingDeletes, setPendingDeletes] = useState<Set<number>>(new Set());

  // Reset session when the source previewPages prop changes (e.g., after Apply).
  useEffect(() => {
    setPages(previewPages);
    setSelected([]);
    setUndoStack([]);
    setRedoStack([]);
    setPendingDeletes(new Set());
  }, [previewPages]);

  const dirty = pendingDeletes.size > 0;

  const handleSelectionChange = (sel: number[]) => {
    setSelected(sel);
  };

  const handleLocalDelete = () => {
    if (selected.length === 0) return;
    if (selected.length === pages.length) {
      // Prevent deleting all pages – backend requires at least one page.
      window.alert('Cannot delete all pages. At least one page must remain.');
      return;
    }
    const newPages = pages.filter(p => !selected.includes(p.page));
    setUndoStack([...undoStack, pages]);
    setRedoStack([]);
    setPages(newPages);
    const newSet = new Set(pendingDeletes);
    selected.forEach(p => newSet.add(p));
    setPendingDeletes(newSet);
    setSelected([]);
  };

  const handleUndo = () => {
    if (undoStack.length === 0) return;
    const previous = undoStack[undoStack.length - 1];
    setUndoStack(undoStack.slice(0, -1));
    setRedoStack([...redoStack, pages]);
    setPages(previous);
    // recompute pending deletes based on difference from original previewPages
    const deleted = new Set<number>();
    previewPages.forEach(p => {
      if (!previous.some((pg: any) => pg.page === p.page)) deleted.add(p.page);
    });
    setPendingDeletes(deleted);
    setSelected([]);
  };

  const handleRedo = () => {
    if (redoStack.length === 0) return;
    const next = redoStack[redoStack.length - 1];
    setRedoStack(redoStack.slice(0, -1));
    setUndoStack([...undoStack, pages]);
    setPages(next);
    const deleted = new Set<number>();
    previewPages.forEach(p => {
      if (!next.some((pg: any) => pg.page === p.page)) deleted.add(p.page);
    });
    setPendingDeletes(deleted);
    setSelected([]);
  };

  const handleApply = () => {
    const deleteArray = Array.from(pendingDeletes);
    if (deleteArray.length === 0) return;
    onChange({
      ...{},
      selected_pages: deleteArray,
      selection_mode: "selected_pages",
      range_start: Math.min(...deleteArray),
      range_end: Math.max(...deleteArray),
    });
    onRun();
    // reset session after applying
    setPages(previewPages);
    setUndoStack([]);
    setRedoStack([]);
    setPendingDeletes(new Set());
    setSelected([]);
  };

  const handleCancel = () => {
    setPages(previewPages);
    setUndoStack([]);
    setRedoStack([]);
    setPendingDeletes(new Set());
    setSelected([]);
  };

  return (
    <PDFOrganizer
      data={pages}
      selectedPages={selected}
      onSelectionChange={handleSelectionChange}
      onDelete={handleLocalDelete}
      onUndo={handleUndo}
      onRedo={handleRedo}
      onApply={handleApply}
      onCancel={handleCancel}
      canUndo={undoStack.length > 0}
      canRedo={redoStack.length > 0}
      dirty={dirty}
    />
  );
}
