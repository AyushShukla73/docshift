import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "DocShift — Document utility workspace",
  description:
    "DocShift is an extensible workspace for converting, merging, splitting and compressing documents.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen font-sans antialiased">{children}</body>
    </html>
  );
}