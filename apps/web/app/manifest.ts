import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "LankaRescue",
    short_name: "LankaRescue",
    description: "Sri Lankan relief coordination portfolio platform",
    start_url: "/",
    display: "standalone",
    background_color: "#f4f7f4",
    theme_color: "#075b52",
    icons: [{ src: "/icon.svg", sizes: "any", type: "image/svg+xml" }],
  };
}

