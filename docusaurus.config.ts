import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

const config: Config = {
  title: "Physical AI & Humanoid Robotics",
  tagline: "A comprehensive guide to modern robotics software development",
  favicon: "img/favicon.ico",

  // GitHub Pages deployment configuration
  url: "https://your-username.github.io",
  baseUrl: "/my-ai-book/",

  // GitHub Pages deployment settings
  organizationName: "your-username", // GitHub org/user name
  projectName: "my-ai-book", // GitHub repo name
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
        docs: {
          sidebarPath: "./sidebars.ts",
          routeBasePath: "/", // Docs as homepage
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
          editUrl:
            "https://github.com/your-username/my-ai-book/tree/main/",
        },
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
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "Book",
        },
        {
          href: "https://github.com/your-username/my-ai-book",
          label: "GitHub",
          position: "right",
        },
      ],
    },

    footer: {
      style: "dark",
      links: [
        {
          title: "Book",
          items: [
            {
              label: "Introduction",
              to: "/intro",
            },
            {
              label: "Glossary",
              to: "/glossary",
            },
            {
              label: "Notation",
              to: "/notation",
            },
          ],
        },
        {
          title: "Modules",
          items: [
            {
              label: "Module 1: ROS 2 Fundamentals",
              to: "/module-1-ros2/introduction",
            },
            {
              label: "Module 2: Digital Twin Simulation",
              to: "/module-2-simulation/gazebo-basics",
            },
            {
              label: "Module 3: NVIDIA Isaac Platform",
              to: "/module-3-isaac/isaac-sim-intro",
            },
            {
              label: "Module 4: Vision-Language-Action",
              to: "/module-4-vla/voice-to-action",
            },
          ],
        },
        {
          title: "More",
          items: [
            {
              label: "GitHub",
              href: "https://github.com/your-username/my-ai-book",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
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
