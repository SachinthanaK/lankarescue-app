"use client";

import { useEffect, useState } from "react";

import { apiBaseUrl, readError, type ReliefRequest } from "@/lib/api";

export function StaffQueue() {
  const [items, setItems] = useState<ReliefRequest[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    fetch(`${apiBaseUrl}/api/v1/demo/staff/relief-requests`)
      .then(async (response) => {
        if (!response.ok) throw new Error(await readError(response));
        return (await response.json()) as ReliefRequest[];
      })
      .then((data) => active && setItems(data))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Unable to load queue."))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, []);

  if (loading) return <p className="empty-state">Loading demo queue…</p>;
  if (error) return <p className="error" role="alert">{error}</p>;
  if (!items.length) return <p className="empty-state">No requests yet. Submit one from the request page.</p>;

  return (
    <div className="queue">
      {items.map((item) => (
        <article className="queue-card" key={item.reference}>
          <div className="queue-heading"><strong>{item.reference}</strong><span className={`status status-${item.status}`}>{item.status}</span></div>
          <h2>{item.needType} · {item.district}</h2>
          <p>{item.description}</p>
          <div className="queue-meta"><span>{item.peopleCount} people</span><span>{item.priority}</span><span>{item.location}</span></div>
          {item.contactValue && <p className="contact">Contact by {item.contactMethod}: {item.contactValue}</p>}
        </article>
      ))}
    </div>
  );
}

