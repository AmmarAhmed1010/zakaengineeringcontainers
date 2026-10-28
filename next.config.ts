import type { NextConfig } from "next";
import catalogueFilenames from "./src/data/catalogue-filenames.json";

const nextConfig: NextConfig = {
  devIndicators: false,
  async redirects() {
    return Object.entries(catalogueFilenames).map(([oldName, newName]) => ({
      source: `/downloads/${oldName}`,
      destination: `/downloads/${newName}`,
      permanent: true,
    }));
  },
};

export default nextConfig;
