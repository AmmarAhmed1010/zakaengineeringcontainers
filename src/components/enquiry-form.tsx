"use client";
import { useState, type FormEvent } from "react";
import { company, services } from "@/data/site";
import { ArrowUpRight } from "./icons";
export function EnquiryForm() {
  const [draft, setDraft] = useState("");
  function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const message = `Hello Zaka Engineering,\n\nMy name is ${data.get("firstName")} ${data.get("lastName")}.\nI am interested in: ${data.get("service")}.\nLocation: ${data.get("location")}\nPhone: ${data.get("phone")}\nEmail: ${data.get("email")}\n\nProject details: ${data.get("message")}`;
    setDraft(`${company.whatsapp}?text=${encodeURIComponent(message)}`);
  }
  return (
    <form
      onSubmit={submit}
      onChange={() => setDraft("")}
      className="enquiry-form"
    >
      <p className="eyebrow">Your next space starts here</p>
      <h2>
        Tell us what you
        <br />
        have in mind.
      </h2>
      <div className="form-grid">
        <label>
          First name
          <input
            required
            name="firstName"
            autoComplete="given-name"
            placeholder="Your first name"
            maxLength={60}
          />
        </label>
        <label>
          Last name
          <input
            required
            name="lastName"
            autoComplete="family-name"
            placeholder="Your last name"
            maxLength={60}
          />
        </label>
        <label>
          Phone number
          <input
            required
            name="phone"
            type="tel"
            inputMode="tel"
            autoComplete="tel"
            placeholder="+92"
            maxLength={30}
          />
        </label>
        <label>
          Email address
          <input
            required
            name="email"
            type="email"
            autoComplete="email"
            placeholder="you@example.com"
            maxLength={150}
          />
        </label>
        <label>
          What are you planning?
          <select required name="service" defaultValue="">
            <option value="" disabled>
              Select a service
            </option>
            {services.map((s) => (
              <option key={s.slug}>{s.title}</option>
            ))}
            <option>Something else</option>
          </select>
        </label>
        <label>
          Project location
          <input
            required
            name="location"
            placeholder="City or site location"
            maxLength={150}
          />
        </label>
        <label className="form-full">
          Tell us about your project
          <textarea
            required
            name="message"
            rows={4}
            placeholder="Your idea, approximate size, budget, or any questions…"
            maxLength={3000}
          />
        </label>
      </div>
      <p className="small muted">
        We’ll prepare your enquiry for WhatsApp. You can review it before
        sending.
      </p>
      <button className="button button-red" type="submit">
        Prepare my enquiry
        <ArrowUpRight />
      </button>
      {draft && (
        <div className="form-feedback" role="status">
          <strong>Your enquiry is ready.</strong>
          <p>Continue to WhatsApp to review and send it to our team.</p>
          <a
            href={draft}
            target="_blank"
            rel="noopener noreferrer"
            className="text-link"
          >
            Continue to WhatsApp
            <ArrowUpRight />
          </a>
        </div>
      )}
    </form>
  );
}
