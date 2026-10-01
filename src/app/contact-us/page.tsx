import type { Metadata } from "next";
import Image from "next/image";
import { PageIntro } from "@/components/ui";
import { EnquiryForm } from "@/components/enquiry-form";
import { ArrowUpRight } from "@/components/icons";
import { company } from "@/data/site";
export const metadata: Metadata = {
  title: "Contact Us",
  description:
    "Talk to Zaka Engineering in Islamabad about your container home, prefab office, or fabrication project. Call +92 340 5221225.",
};
export default function Contact() {
  return (
    <main id="main-content">
      <PageIntro
        eyebrow="Start a conversation"
        title="Big ideas start here."
        text="Have a space in mind? We’d love to hear about it. Reach out, visit us, or send your project brief."
      />
      <div className="container contact-grid">
        <aside className="contact-details">
          <div>
            <p className="eyebrow">Call or WhatsApp</p>
            <a className="contact-phone" href={company.phoneHref}>
              {company.phone}
            </a>
            <br />
            <a
              href={company.whatsapp}
              target="_blank"
              rel="noopener noreferrer"
              className="text-link"
            >
              Chat with our team
              <ArrowUpRight />
            </a>
          </div>
          <div>
            <h3>Find us in Islamabad.</h3>
            <p>{company.address}</p>
            <a
              href={company.maps}
              className="text-link"
              target="_blank"
              rel="noopener noreferrer"
            >
              Get directions
              <ArrowUpRight />
            </a>
          </div>
          <div>
            <h3>Office hours.</h3>
            <p>
              Monday–Saturday / 9:00 am–6:00 pm
              <br />
              Friday / Closed
            </p>
            <a href={`mailto:${company.email}`}>{company.email}</a>
          </div>
          <div className="contact-image image-frame">
            <Image
              src="/images/generated/office.webp"
              alt="Concept for a modular Zaka office"
              fill
              sizes="40vw"
            />
          </div>
        </aside>
        <EnquiryForm />
      </div>
    </main>
  );
}
