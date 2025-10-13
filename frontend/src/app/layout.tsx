import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { SkipLink } from "@/components/ui";
import { LoadingProvider } from "@/contexts/LoadingContext";
import { ErrorProvider } from "@/contexts/ErrorContext";
import { GlobalLoading } from "@/components/GlobalLoading";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "My TODO App",
  description: "Organize your tasks and boost your productivity",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ErrorProvider>
          <LoadingProvider>
            <SkipLink href="#main-content">Skip to main content</SkipLink>
            <SkipLink href="#navigation">Skip to navigation</SkipLink>
            <GlobalLoading />
            {children}
          </LoadingProvider>
        </ErrorProvider>
      </body>
    </html>
  );
}
