import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/sections/navbar";


export const metadata: Metadata = {
  title: "DevKit",
  description:
    "Modern Developer CLI Toolkit",
};


export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {

  return (
    <html lang="en">

      <body>
        <Navbar />
        {children}

      </body>

    </html>
  );
}