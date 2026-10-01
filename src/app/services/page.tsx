import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { PageIntro } from "@/components/ui";
import { ProjectCTA } from "@/components/footer";
import { ArrowUpRight } from "@/components/icons";
import { services } from "@/data/site";
export const metadata: Metadata = {
  title: "Our Services",
  description:
    "Prefab cabins, shipping container conversions, customized containers, aluminum, mild-steel and stainless-steel fabrication across Pakistan.",
};
export default function Services() {
  return (
    <main id="main-content">
      <PageIntro
        eyebrow="Our expertise"
        title="Made for your next idea."
        text="Six specialist services. One team to bring your project together, from design to fabrication and delivery."
      />
      <section className="container service-list">
        {services.map((s, i) => (
          <article className="service-row" key={s.slug}>
            <span className="row-number">0{i + 1}</span>
            <div>
              <h2>{s.title}</h2>
              <p>{s.description}</p>
              <div className="tags">
                {s.tags.map((t) => (
                  <span key={t}>{t}</span>
                ))}
              </div>
              <Link href={`/services/${s.slug}`} className="text-link">
                Explore this service
                <ArrowUpRight />
              </Link>
            </div>
            <Link
              href={`/services/${s.slug}`}
              className="service-photo"
              aria-label={`Explore ${s.title}`}
            >
              <Image
                src={s.image}
                alt={`${s.title} concept illustration`}
                fill
                sizes="(max-width:640px) 100vw, 45vw"
              />
              <span className="concept-label">Concept visualization</span>
              <span className="image-arrow">
                <ArrowUpRight />
              </span>
            </Link>
          </article>
        ))}
      </section>
      <ProjectCTA />
    </main>
  );
}
