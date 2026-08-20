"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";

import { apiBaseUrl, readError } from "@/lib/api";

const districts = [
  "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle", "Gampaha",
  "Hambantota", "Jaffna", "Kalutara", "Kandy", "Kegalle", "Kilinochchi", "Kurunegala",
  "Mannar", "Matale", "Matara", "Monaragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa",
  "Puttalam", "Ratnapura", "Trincomalee", "Vavuniya",
];

type Created = {
  reference: string;
  trackingToken: string;
  message: string;
};

export function RequestForm() {
  const [created, setCreated] = useState<Created | null>(null);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError("");
    const form = new FormData(event.currentTarget);
    const body = {
      district: form.get("district"),
      location: form.get("location"),
      needType: form.get("needType"),
      peopleCount: Number(form.get("peopleCount")),
      priority: form.get("priority"),
      description: form.get("description"),
      contactMethod: form.get("contactMethod"),
      contactValue: form.get("contactValue"),
    };
    try {
      const response = await fetch(`${apiBaseUrl}/api/v1/relief-requests`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!response.ok) throw new Error(await readError(response));
      const result = (await response.json()) as Created;
      setCreated(result);
      localStorage.setItem(
        "lankarescue-last-request",
        JSON.stringify({ reference: result.reference, trackingToken: result.trackingToken }),
      );
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to submit the request.");
    } finally {
      setSubmitting(false);
    }
  }

  if (created) {
    return (
      <section className="result-card" aria-live="polite">
        <span className="eyebrow">Request submitted</span>
        <h2>Save both private tracking details</h2>
        <dl className="credentials">
          <div><dt>Reference</dt><dd>{created.reference}</dd></div>
          <div><dt>Private token</dt><dd className="token">{created.trackingToken}</dd></div>
        </dl>
        <p>{created.message}</p>
        <p className="privacy-note">The token is shown once and is not stored by the API. Do not share it publicly.</p>
        <Link className="button" href="/track">Track this request</Link>
      </section>
    );
  }

  return (
    <form className="form-card" onSubmit={submit}>
      <div className="field-grid">
        <label>District<select name="district" required defaultValue=""><option value="" disabled>Select district</option>{districts.map((district) => <option key={district}>{district}</option>)}</select></label>
        <label>Nearest location<input name="location" required minLength={2} maxLength={120} placeholder="Town, landmark or shelter" /></label>
        <label>Type of help<select name="needType" required defaultValue="water"><option value="food">Food</option><option value="water">Water</option><option value="medical">Medical</option><option value="shelter">Shelter</option><option value="evacuation">Evacuation</option><option value="other">Other</option></select></label>
        <label>Number of people<input name="peopleCount" required type="number" min={1} max={500} defaultValue={1} /></label>
        <label>Priority<select name="priority" required defaultValue="normal"><option value="normal">Normal</option><option value="urgent">Urgent</option><option value="critical">Critical</option></select></label>
        <label>Preferred contact<select name="contactMethod" required defaultValue="phone"><option value="phone">Phone call</option><option value="sms">SMS</option><option value="email">Email</option></select></label>
      </div>
      <label>Contact detail<input name="contactValue" required minLength={2} maxLength={120} autoComplete="tel" placeholder="Phone number or email" /></label>
      <label>Describe what is needed<textarea name="description" required minLength={10} maxLength={2000} rows={5} placeholder="Include important access, safety, medical, or mobility details." /></label>
      {error && <p className="error" role="alert">{error}</p>}
      <button disabled={submitting} type="submit">{submitting ? "Submitting…" : "Submit relief request"}</button>
      <p className="privacy-note">Only provide information needed for responders to contact and assist you.</p>
    </form>
  );
}

