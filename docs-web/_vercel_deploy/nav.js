const links = [
  { href: "/", label: "Inicio" },
  { href: "/que-es.html", label: "Qué es Talaria" },
  { href: "/organismos.html", label: "Órganos" },
  { href: "/spine.html", label: "SPINE" },
  { href: "/forge.html", label: "FORGE" },
  { href: "/axon.html", label: "AXON" },
  { href: "/cli.html", label: "CLI & MCP" },
  { href: "/garantias.html", label: "Garantías A–F" },
  { href: "/quickstart.html", label: "Quickstart" },
  { href: "/futuro.html", label: "Futuro" },
];

const el = document.getElementById("nav");
if (el) {
  const path = location.pathname.replace(/index\.html$/, "/") || "/";
  el.innerHTML =
    `<a class="brand" href="/">Talaria</a><div class="brand-sub">SkillGraph COS · SGCOS</div>` +
    links
      .map((l) => {
        const active =
          path === l.href ||
          (l.href !== "/" && path.endsWith(l.href.replace(/^\//, "")));
        return `<a href="${l.href}" class="${active ? "active" : ""}">${l.label}</a>`;
      })
      .join("");
}
