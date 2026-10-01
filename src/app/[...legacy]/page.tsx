import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import archive from "@/data/archive.json";
import { PageIntro } from "@/components/ui";
import { ArrowUpRight } from "@/components/icons";
const owned = ["home", "about-us", "services", "projects", "contact-us"];
const legacy = archive.filter(
  (p) => !owned.includes(p.slug) && !p.slug.startsWith("projects/"),
);
export const metadata: Metadata = { robots: { index: false, follow: false } };
export function generateStaticParams() {
  return legacy.map((p) => ({ legacy: p.slug.split("/") }));
}
export default async function Legacy({
  params,
}: {
  params: Promise<{ legacy: string[] }>;
}) {
  const { legacy: segments } = await params;
  const p = archive.find((p) => p.slug === segments.join("/"));
  if (!p) notFound();
  return (
    <main id="main-content">
      <PageIntro
        eyebrow="Company archive"
        title={p.title}
        text="Original website information, preserved for reference."
      />
      <div className="container">
        <div className="archive-text">{p.body}</div>
        <Link
          href="/contact-us"
          className="text-link"
          style={{ marginBottom: 60 }}
        >
          Discuss your requirements
          <ArrowUpRight />
        </Link>
      </div>
    </main>
  );
}
