"use client";

import { FormEvent, useState } from "react";

import { apiBaseUrl, readError, type ReliefRequest } from "@/lib/api";

export function TrackForm() {
  const [reference, setReference] = useState("");
  const [trackingToken, setTrackingToken] = useState("");
  const [result, setResult] = useState<ReliefRequest | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function loadSavedRequest() {
    try {
      const value = localStorage.getItem("lankarescue-last-request");
      if (!value) return;
      const saved = JSON.parse(value) as { reference: string; trackingToken: string };
      setReference(saved.reference);
      setTrackingToken(saved.trackingToken);
    } catch {
      localStorage.removeItem("lankarescue-last-request");
    }
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    const form = new FormData(event.currentTarget);
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/relief-requests/track`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reference: form.get("reference"), trackingToken: form.get("trackingToken") }),
      });
      if (!response.ok) throw new Error(await readError(response));
      setResult((await response.json()) as ReliefRequest);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to track the request.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <form className="form-card compact" onSubmit={submit}>
        <button className="button secondary" type="button" onClick={loadSavedRequest}>Use last submitted request</button>
        <label>Request reference<input name="reference" required value={reference} onChange={(event) => setReference(event.target.value)} placeholder="REQ-2026-XXXXXXXX" autoCapitalize="characters" /></label>
        <label>Private tracking token<input name="trackingToken" required minLength={32} value={trackingToken} onChange={(event) => setTrackingToken(event.target.value)} type="password" autoComplete="off" /></label>
        {error && <p className="error" role="alert">{error}</p>}
        <button disabled={loading} type="submit">{loading ? "Checking…" : "Check status"}</button>
      </form>
      {result && (
        <section className="result-card" aria-live="polite">
          <span className={`status status-${result.status}`}>{result.status}</span>
          <h2>{result.reference}</h2>
          <p>{result.description}</p>
          <dl className="summary-grid">
            <div><dt>District</dt><dd>{result.district}</dd></div>
            <div><dt>Location</dt><dd>{result.location}</dd></div>
            <div><dt>People</dt><dd>{result.peopleCount}</dd></div>
            <div><dt>Priority</dt><dd>{result.priority}</dd></div>
          </dl>
        </section>
      )}
    </>
  );
}

