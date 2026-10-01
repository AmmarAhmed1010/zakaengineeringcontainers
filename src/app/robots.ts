import type { MetadataRoute } from "next";
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: [
        "/source-content/",
        "/all-team/",
        "/all-project/",
        "/all-service/",
        "/author/",
        "/pricing",
        "/blog",
        "/blog-grid",
        "/team-members",
        "/faq",
      ],
    },
    sitemap: "https://zakaengineeringcontainers.com/sitemap.xml",
  };
}
