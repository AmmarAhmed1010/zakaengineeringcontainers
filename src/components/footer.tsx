import Image from "next/image";
import Link from "next/link";
import { company } from "@/data/site";
import { ArrowUpRight } from "./icons";
export function ProjectCTA() {
  return (
    <section className="project-cta">
      <div className="container cta-inner">
        <div>
          <p className="eyebrow light">The next space is yours</p>
          <h2>
            Let’s build something
            <br />
            that moves you.
          </h2>
        </div>
        <div>
          <p>
            A home. A workplace. A new idea.
            <br />
            Tell us what you have in mind.
          </p>
          <Link className="button button-white" href="/contact-us">
            Start a conversation
            <ArrowUpRight />
          </Link>
        </div>
      </div>
    </section>
  );
}
export function Footer() {
  return (
    <footer className="footer">
      <div className="container footer-grid">
        <div className="footer-brand">
          <Link href="/" aria-label="Zaka Engineering home">
            <Image
              src="/images/original/Containers-Prefab.svg"
              alt="Zaka Engineering"
              width={200}
              height={80}
            />
          </Link>
          <p>
            Custom container solutions.
            <br />
            Homes. Offices. Workshops. Site units.
            <br />
            Serving across Pakistan.
          </p>
          <div className="socials">
            {company.socials.map((s) => (
              <a
                key={s.name}
                href={s.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                {s.name}
                <ArrowUpRight width={12} height={12} />
              </a>
            ))}
          </div>
        </div>
        <div>
          <p className="footer-label">Explore</p>
          {[
            { label: "Our story", href: "/about-us" },
            { label: "Our services", href: "/services" },
            { label: "Our projects", href: "/projects" },
            { label: "Design catalogues", href: "/downloads" },
            { label: "Contact us", href: "/contact-us" },
          ].map((l) => (
            <Link key={l.href} href={l.href}>
              {l.label}
            </Link>
          ))}
        </div>
        <div>
          <p className="footer-label">Visit us</p>
          <a
            href={company.maps}
            target="_blank"
            rel="noopener noreferrer"
            className="address"
          >
            {company.address}
            <ArrowUpRight width={15} />
          </a>
          <p className="small muted">
            Monday–Saturday, 9:00 am–6:00 pm
            <br />
            Friday closed
          </p>
        </div>
        <div>
          <p className="footer-label">Let’s talk</p>
          <a className="footer-phone" href={company.phoneHref}>
            {company.phone}
          </a>
          <a href={`mailto:${company.email}`}>{company.email}</a>
          <a
            href={company.whatsapp}
            target="_blank"
            rel="noopener noreferrer"
            className="text-link"
          >
            Chat on WhatsApp
            <ArrowUpRight />
          </a>
        </div>
      </div>
      <div className="container footer-bottom">
        <span>
          © {new Date().getFullYear()} {company.legalName}
        </span>
        <Link href="/source-content">Content archive</Link>
        <span>Designed to go further.</span>
      </div>
    </footer>
  );
}
