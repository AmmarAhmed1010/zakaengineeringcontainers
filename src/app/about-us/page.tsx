import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { PageIntro, SectionTitle } from "@/components/ui";
import { ProjectCTA } from "@/components/footer";
import { ArrowUpRight } from "@/components/icons";
export const metadata: Metadata = {
  title: "Our Story",
  description:
    "Meet Zaka Engineering, container and prefab specialists led by Zaka-ur-Rehman in Islamabad.",
};
export default function About() {
  return (
    <main id="main-content">
      <PageIntro
        eyebrow="Our story"
        title="A better way to build."
        text="Practical engineering. Thoughtful design. A team that sees the possibility in every container."
      />
      <div className="container page-banner image-frame">
        <Image
          src="/images/generated/hero.webp"
          alt="Container home architectural concept"
          fill
          sizes="100vw"
          loading="eager"
        />
        <span className="concept-label">Residential concept</span>
      </div>
      <section className="container section-pad about-story">
        <div>
          <p className="eyebrow">
            <span />
            Prefab experts
          </p>
          <h2>
            Create the building
            <br />
            you want <span className="serif-word">here.</span>
          </h2>
        </div>
        <div>
          <p>
            From container homes to prefab offices and commercial spaces — we
            design and deliver exactly what you need, where you need it. With a
            strong focus on customer satisfaction and structural quality, we
            ensure every project reflects our commitment to smart and
            sustainable building.
          </p>
          <p>
            With 5+ years of hands-on experience, Zaka Engineering specializes
            in transforming shipping containers into fully functional homes,
            cafes, restaurants, site offices, and guard cabins. We focus on
            quality craftsmanship, modern design and fast project delivery to
            help you build smarter spaces with less hassle and more impact.
          </p>
          <ul className="about-values">
            <li>Client-focused planning & execution</li>
            <li>Transparent timelines — no surprises</li>
            <li>
              Proven expertise in prefab & container construction across
              Pakistan
            </li>
          </ul>
          <div className="founder-signature">
            <strong>Zaka-ur-Rehman</strong>
            <p>CEO / Zaka Engineering</p>
          </div>
        </div>
      </section>
      <section className="services-preview section-pad">
        <div className="container">
          <SectionTitle
            eyebrow="What guides us"
            title="Smart spaces. Strong relationships."
          />
          <div className="values-grid">
            <div>
              <span>01 / Quality craftsmanship</span>
              <h3>Built with care.</h3>
              <p>
                Our skilled team brings attention to the structural work,
                finishes, and practical details that make a container space
                functional.
              </p>
            </div>
            <div>
              <span>02 / Nationwide services</span>
              <h3>Where you need us.</h3>
              <p>
                We proudly serve clients across Islamabad, Rawalpindi and all
                major cities in Pakistan — delivering top-quality container
                units to your doorstep.
              </p>
            </div>
            <div>
              <span>03 / Trusted by clients</span>
              <h3>A shared vision.</h3>
              <p>
                Our commitment to quality and innovation has earned us trust
                across industries — from builders to business owners and
                individuals alike.
              </p>
            </div>
          </div>
          <Link
            href="/services"
            className="text-link"
            style={{ marginTop: 35 }}
          >
            Explore our service solutions
            <ArrowUpRight />
          </Link>
        </div>
      </section>
      <ProjectCTA />
    </main>
  );
}
