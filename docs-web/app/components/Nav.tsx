"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Inicio" },
  { href: "/que-es", label: "Qué es Mímir" },
  { href: "/organismos", label: "Órganos" },
  { href: "/spine", label: "SPINE" },
  { href: "/forge", label: "FORGE" },
  { href: "/axon", label: "AXON" },
  { href: "/cli", label: "CLI & MCP" },
  { href: "/garantias", label: "Garantías A–F" },
  { href: "/quickstart", label: "Quickstart" },
  { href: "/futuro", label: "Futuro" },
];

export function Nav() {
  const path = usePathname();
  return (
    <aside className="nav">
      <Link href="/" className="brand">
        Mímir
      </Link>
      <div className="brand-sub">SkillGraph COS · SGCOS</div>
      {links.map((l) => (
        <Link
          key={l.href}
          href={l.href}
          className={path === l.href ? "active" : undefined}
        >
          {l.label}
        </Link>
      ))}
    </aside>
  );
}
