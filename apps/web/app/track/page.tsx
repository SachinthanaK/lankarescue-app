import type { Metadata } from "next";

import { TrackForm } from "@/components/track-form";

export const metadata: Metadata = { title: "Track request" };

export default function TrackPage() {
  return <section className="page-shell narrow"><span className="eyebrow">Private status lookup</span><h1>Track a relief request</h1><p className="page-intro">Both values are required. The private token is sent in the request body so it does not appear in browser URLs or ordinary access logs.</p><TrackForm /></section>;
}

