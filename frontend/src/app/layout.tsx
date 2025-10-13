import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { SkipLink } from "@/components/ui";
import { LoadingProvider } from "@/contexts/LoadingContext";
import { ErrorProvider } from "@/contexts/ErrorContext";
import { GlobalLoading } from "@/components/GlobalLoading";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
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
        className={`${inter.variable} ${jetbrainsMono.variable} antialiased`}
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
