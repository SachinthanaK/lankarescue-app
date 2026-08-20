"use client";

import { useEffect } from "react";

export function ServiceWorkerRegistration() {
  useEffect(() => {
    if (!("serviceWorker" in navigator) || process.env.NODE_ENV !== "production") return;
    navigator.serviceWorker.register("/sw.js").catch(() => {
      // Installation is optional; the network application remains fully usable.
    });
  }, []);

  return null;
}

