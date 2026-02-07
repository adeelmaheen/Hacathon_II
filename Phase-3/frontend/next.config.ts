import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  // Configure webpack to resolve modules from the frontend directory first
  // This fixes the issue where tailwindcss was being resolved from the parent directory
  webpack: (config, { isServer }) => {
    config.resolve.modules = [
      path.resolve(__dirname, "node_modules"),
      ...(config.resolve.modules || []),
    ];
    return config;
  },
  // Configure Turbopack as fallback (when not using --webpack flag)
  turbopack: {
    resolveAlias: {
      // Ensure tailwindcss resolves from the frontend directory
      tailwindcss: path.resolve(__dirname, "node_modules/tailwindcss"),
    },
  },
};

export default nextConfig;
