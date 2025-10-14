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
  display: "swap",
  weight: ["400", "500", "600", "700"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Remember The Milk... And Everything Else",
  description: "A beautiful, modern task management app to organize your life",
  icons: {
    icon: [
      { url: '/favicon.svg', type: 'image/svg+xml' },
    ],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.variable} ${jetbrainsMono.variable} font-sans antialiased`}
        style={{ fontFamily: 'var(--font-inter)' }}
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
