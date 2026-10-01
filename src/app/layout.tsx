import type { Metadata } from "next";
import { DM_Sans, Manrope } from "next/font/google";
import { Header } from "@/components/header";
import { Footer } from "@/components/footer";
import { company } from "@/data/site";
import "./globals.css";

const bodyFont = DM_Sans({
  variable: "--font-body",
  subsets: ["latin"],
});

const displayFont = Manrope({
  variable: "--font-display",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://zakaengineeringcontainers.com"),
  title: {
    default: "Zaka Engineering | Container Spaces, Endless Possibilities",
    template: "%s | Zaka Engineering",
  },
  description:
    "Custom container homes, site offices, cafes, prefab cabins, and metal fabrication. Designed in Islamabad and delivered across Pakistan.",
  openGraph: {
    title: "Zaka Engineering | Built for Life. Engineered to Move.",
    description: "Thoughtful container and prefab spaces across Pakistan.",
    images: [{ url: "/images/generated/hero.webp" }],
    type: "website",
    locale: "en_PK",
  },
  icons: { icon: "/images/original/cropped-LOGO-ZAKA-ENGINEERING-1-32x32.png" },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      data-scroll-behavior="smooth"
      className={`${bodyFont.variable} ${displayFont.variable} h-full antialiased`}
    >
      <body>
        <a className="skip-link" href="#main-content">
          Skip to content
        </a>
        <Header />
        {children}
        <Footer />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Organization",
              name: company.legalName,
              url: "https://zakaengineeringcontainers.com",
              logo: "https://zakaengineeringcontainers.com/images/original/LOGO-ZAKA-ENGINEERING-1.png",
              telephone: company.phone,
              email: company.email,
              sameAs: company.socials.map((s) => s.url),
              address: {
                "@type": "PostalAddress",
                streetAddress: company.address,
                addressLocality: "Islamabad",
                addressCountry: "PK",
              },
              areaServed: "Pakistan",
            }).replace(/</g, "\\u003c"),
          }}
        />
      </body>
    </html>
  );
}
