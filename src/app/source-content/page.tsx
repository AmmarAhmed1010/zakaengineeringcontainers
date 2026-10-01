import type { Metadata } from "next";
import Link from "next/link";
import archive from "@/data/archive.json";
import { PageIntro } from "@/components/ui";
import { ArrowUpRight } from "@/components/icons";
export const metadata: Metadata = {
  title: "Original Content Archive",
  robots: { index: false, follow: false },
};
export default function Archive() {
  return (
    <main id="main-content">
      <PageIntro
        eyebrow="Original website content"
        title="The complete archive."
        text="The original website’s page content is retained here for reference, including older template material. It is reproduced as supplied."
      />
      <div className="container archive-grid">
        {archive.map((p) => (
          <Link key={p.slug} href={`/source-content/${p.slug}`}>
            {p.title}
            <ArrowUpRight />
          </Link>
        ))}
      </div>
    </main>
  );
}
