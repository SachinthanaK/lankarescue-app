import type { Metadata } from "next";

import { StaffQueue } from "@/components/staff-queue";

export const metadata: Metadata = { title: "Demo staff queue" };

export default function StaffPage() {
  return <section className="page-shell"><span className="eyebrow">Local development only</span><h1>Relief operations queue</h1><p className="page-intro">This temporary view deliberately works only when the API runs in local demo mode. Staff authentication and authorization arrive before any shared environment.</p><StaffQueue /></section>;
}

