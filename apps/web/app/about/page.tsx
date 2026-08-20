import type { Metadata } from "next";

export const metadata: Metadata = { title: "About" };

export default function AboutPage() {
  return (
    <section className="page-shell narrow prose">
      <span className="eyebrow">About the project</span>
      <h1>A production-minded DevOps portfolio</h1>
      <p>LankaRescue is an educational implementation of a national-scale relief coordination platform. It demonstrates secure software design, platform engineering, GitOps, observability, reliability, and controlled delivery.</p>
      <h2>Phase 1 boundaries</h2>
      <p>The current release is intentionally local and English-only. Data is in memory, staff access is a gated demo, notifications are not delivered, and it must not be used for real emergency response.</p>
      <h2>Privacy</h2>
      <p>The citizen tracking token is generated with strong randomness, stored only as a one-way hash by the API, and excluded from URLs and logs.</p>
    </section>
  );
}

