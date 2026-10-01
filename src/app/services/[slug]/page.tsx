import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { services, process } from "@/data/site";
import { PageIntro, SectionTitle } from "@/components/ui";
import { ProjectCTA } from "@/components/footer";
import { ArrowUpRight } from "@/components/icons";
export function generateStaticParams() {
  return services.map((s) => ({ slug: s.slug }));
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const s = services.find((s) => s.slug === slug);
  return { title: s?.title, description: s?.description };
}
export default async function Service({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const s = services.find((s) => s.slug === slug);
  if (!s) notFound();
  return (
    <main id="main-content">
      <PageIntro eyebrow="Specialist services" title={s.title} text={s.short} />
      <div className="container page-banner image-frame">
        <Image
          src={s.image}
          alt={`${s.title}, architectural concept`}
          fill
          sizes="100vw"
          loading="eager"
        />
        <span className="concept-label">Concept visualization</span>
      </div>
      <section className="container section-pad detail-grid">
        <div>
          <p className="eyebrow">
            <span />
            Built around your needs
          </p>
          <h2>{s.short}</h2>
          <div className="tags">
            {s.tags.map((t) => (
              <span key={t}>{t}</span>
            ))}
          </div>
        </div>
        <div>
          <p>{s.description}</p>
          <p>{s.detail}</p>
          <p>
            Our services are available in Islamabad, Rawalpindi, and across
            Pakistan. Talk to us about your site, timeline, and the details that
            matter to you.
          </p>
          <Link
            href={`/contact-us?service=${s.slug}`}
            className="button button-red"
          >
            Discuss your project
            <ArrowUpRight />
          </Link>
        </div>
      </section>
      <section className="services-preview section-pad">
        <div className="container">
          <SectionTitle
            eyebrow="How we work"
            title="Considered from start to finish."
          />
          <div className="process-grid">
            {process.map((p, i) => (
              <div key={p.title}>
                <span className="process-number">0{i + 1}</span>
                <h3>{p.title}</h3>
                <p>{p.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      <ProjectCTA />
    </main>
  );
}
