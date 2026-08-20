import type { Metadata, Viewport } from "next";

import { ServiceWorkerRegistration } from "@/components/service-worker-registration";
import { SiteHeader } from "@/components/site-header";

import "./globals.css";

export const metadata: Metadata = {
  title: { default: "LankaRescue", template: "%s · LankaRescue" },
  description: "A resilient relief coordination portfolio platform for Sri Lanka.",
  applicationName: "LankaRescue",
};

export const viewport: Viewport = { themeColor: "#075b52", width: "device-width", initialScale: 1 };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <ServiceWorkerRegistration />
        <SiteHeader />
        <main>{children}</main>
        <footer><span>LankaRescue portfolio project</span><span>Built for resilient, observable delivery</span></footer>
      </body>
    </html>
  );
}

