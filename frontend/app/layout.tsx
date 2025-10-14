import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FinLit AI - Financial Literacy Companion",
  description: "AI-powered financial guidance",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
