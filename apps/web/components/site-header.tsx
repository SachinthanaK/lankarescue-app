import Link from "next/link";

import { getMessages } from "@/lib/messages";

export function SiteHeader() {
  const text = getMessages();
  return (
    <>
      <div className="demo-banner" role="status">
        {text.demo}
      </div>
      <header className="site-header">
        <Link className="brand" href="/" aria-label="LankaRescue home">
          <span className="brand-mark" aria-hidden="true">LR</span>
          {text.brand}
        </Link>
        <nav aria-label="Primary navigation">
          <Link href="/request">Request</Link>
          <Link href="/track">Track</Link>
          <Link href="/staff">Staff demo</Link>
          <Link href="/about">About</Link>
        </nav>
      </header>
    </>
  );
}

