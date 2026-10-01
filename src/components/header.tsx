"use client";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { ArrowUpRight } from "./icons";
import { company } from "@/data/site";
const links = [
  { title: "Home", href: "/" },
  { title: "About us", href: "/about-us" },
  { title: "Services", href: "/services" },
  { title: "Projects", href: "/projects" },
  { title: "Downloads", href: "/downloads" },
];
export function Header() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  return (
    <>
      <div className="utility-bar">
        <div className="container utility-inner">
          <span>Designed in Islamabad. Delivered across Pakistan.</span>
          <a href={company.phoneHref}>
            Let’s talk <span className="utility-phone">{company.phone}</span>
            <ArrowUpRight width={13} height={13} />
          </a>
        </div>
      </div>
      <header className="header">
        <div className="container nav-inner">
          <Link
            href="/"
            className="brand"
            aria-label="Zaka Engineering home"
            onClick={() => setOpen(false)}
          >
            <Image
              src="/images/original/Containers-Prefab.svg"
              alt="Zaka Engineering Containers & Prefab"
              width={200}
              height={80}
              loading="eager"
            />
          </Link>
          <nav aria-label="Main navigation" className="desktop-nav">
            {links.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className={
                  pathname === l.href ||
                  (l.href !== "/" && pathname.startsWith(l.href))
                    ? "active"
                    : ""
                }
              >
                {l.title}
              </Link>
            ))}
          </nav>
          <Link className="button button-red nav-cta" href="/contact-us">
            Start your project
            <ArrowUpRight />
          </Link>
          <button
            className="menu-toggle"
            aria-label={open ? "Close navigation" : "Open navigation"}
            aria-expanded={open}
            aria-controls={open ? "mobile-navigation" : undefined}
            onClick={() => setOpen(!open)}
          >
            {open ? (
              <span className="close-icon">×</span>
            ) : (
              <span className="hamburger">
                <i />
                <i />
              </span>
            )}
          </button>
        </div>
        {open && (
          <nav
            id="mobile-navigation"
            aria-label="Mobile navigation"
            className="mobile-nav"
          >
            {[...links, { title: "Contact us", href: "/contact-us" }].map(
              (l) => (
                <Link href={l.href} key={l.href} onClick={() => setOpen(false)}>
                  {l.title}
                  <ArrowUpRight />
                </Link>
              ),
            )}
          </nav>
        )}
      </header>
    </>
  );
}
