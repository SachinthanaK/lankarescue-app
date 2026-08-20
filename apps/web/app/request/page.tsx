import type { Metadata } from "next";

import { RequestForm } from "@/components/request-form";

export const metadata: Metadata = { title: "Request relief" };

export default function RequestPage() {
  return <section className="page-shell"><span className="eyebrow">Citizen request</span><h1>Tell us what is needed</h1><p className="page-intro">Provide only the information responders need. This Phase 1 demo stores requests in memory and clears them when the API restarts.</p><RequestForm /></section>;
}

