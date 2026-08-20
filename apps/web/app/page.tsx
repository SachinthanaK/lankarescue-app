import Link from "next/link";

import { getMessages } from "@/lib/messages";

export default function Home() {
  const text = getMessages();
  return (
    <>
      <section className="hero">
        <div>
          <span className="eyebrow">Relief coordination, made visible</span>
          <h1>Ask for help. Track the response.</h1>
          <p className="lead">LankaRescue connects citizen relief requests with a transparent operations workflow designed for Sri Lankan disaster response.</p>
          <div className="actions"><Link className="button" href="/request">{text.requestHelp}</Link><Link className="button secondary" href="/track">{text.trackRequest}</Link></div>
        </div>
        <aside className="safety-card"><span aria-hidden="true">!</span><div><strong>Emergency notice</strong><p>{text.emergency}</p></div></aside>
      </section>
      <section className="feature-grid" aria-label="How LankaRescue works">
        <article><span>01</span><h2>Submit</h2><p>Share the minimum details responders need to understand a relief request.</p></article>
        <article><span>02</span><h2>Track securely</h2><p>Use a public reference plus a separate private token. Tokens are never stored in plaintext.</p></article>
        <article><span>03</span><h2>Coordinate</h2><p>A compact local staff view demonstrates the operational queue before identity arrives.</p></article>
      </section>
    </>
  );
}

