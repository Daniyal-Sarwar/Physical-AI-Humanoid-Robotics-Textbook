import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

const config: Config = {
  title: "Physical AI & Humanoid Robotics",
  tagline: "A comprehensive guide to modern robotics software development",
  favicon: "img/favicon.ico",

  // GitHub Pages deployment configuration
  url: "https://daniyal-sarwar.github.io",
  baseUrl: "/Physical-AI-Humanoid-Robotics-Textbook/",

  // GitHub Pages deployment settings
  organizationName: "Daniyal-Sarwar", // GitHub org/user name
  projectName: "Physical-AI-Humanoid-Robotics-Textbook", // GitHub repo name
  deploymentBranch: "gh-pages",
  trailingSlash: false,

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  // Math rendering support
  stylesheets: [
    {
      href: "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css",
      type: "text/css",
      integrity:
        "sha384-n8MVd4RsNIU0tAv4ct0nTaAbDJwPJzDEaqSD1odI+WdtXRGWt2kTvGFasHpSy3SV",
      crossorigin: "anonymous",
    },
  ],

  presets: [
    [
      "classic",
      {
        docs: false, // Disabled - docs folder removed
        blog: false, // Disable blog
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Social card image
    image: "img/social-card.jpg",
    
    navbar: {
      title: "Physical AI Textbook",
      logo: {
        alt: "Physical AI Textbook Logo",
        src: "img/logo.svg",
      },
      items: [
        {
          href: "https://github.com/Daniyal-Sarwar/Physical-AI-Humanoid-Robotics-Textbook",
          label: "GitHub",
          position: "right",
        },
      ],
    },

    footer: {
      style: "dark",
      links: [
        {
          title: "More",
          items: [
            {
              label: "GitHub",
              href: "https://github.com/Daniyal-Sarwar/Physical-AI-Humanoid-Robotics-Textbook",
            },
            {
              label: "Author: Daniyal Sarwar",
              href: "https://github.com/Daniyal-Sarwar",
            },
          ],
        },
      ],
      copyright: `Physical AI Textbook™ — Copyright © ${new Date().getFullYear()} Created by Daniyal Sarwar. Built with Docusaurus.`,
    },

    prism: {
      theme: require("prism-react-renderer").themes.github,
      darkTheme: require("prism-react-renderer").themes.dracula,
      additionalLanguages: ["python", "cpp", "yaml", "bash", "json"],
    },

    // Table of contents depth
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 4,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
