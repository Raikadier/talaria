"""Batch-create standard large-company software team agents via FORGE Builder 2.0.

User-owned graph — not Talaria product canon. Idempotent with force=False (unique suffix).
"""
from __future__ import annotations

from pathlib import Path

from talaria_cli.cmds.forge_build import build_profile_from_brief
from talaria_cli.vault import find_vault

# (id, brief, kind, invocable_by, invokes, mode)
AGENTS: list[tuple[str, str, str, list[str], list[str], str]] = [
    # --- Product ---
    (
        "product-manager",
        "product manager de software: prioriza valor, roadmap y outcomes de negocio",
        "orchestrator",
        [],
        [
            "product-owner",
            "business-analyst",
            "product-designer",
            "ux-designer",
            "scrum-master",
            "tech-lead",
        ],
        "open",
    ),
    (
        "product-owner",
        "product owner agile: backlog, acceptance criteria y maximizar valor del sprint",
        "specialist",
        ["product-manager", "scrum-master", "tech-lead"],
        [],
        "open",
    ),
    (
        "business-analyst",
        "business analyst: elicita requisitos, casos de uso y reglas de negocio auditables",
        "specialist",
        ["product-manager", "product-owner", "software-architect"],
        [],
        "open",
    ),
    (
        "product-designer",
        "product designer: define experiencia de producto end-to-end alineada a outcomes",
        "both",
        ["product-manager", "product-owner"],
        ["ux-designer", "ui-designer", "ux-researcher"],
        "open",
    ),
    # --- Design ---
    (
        "ux-designer",
        "ux designer: flujos, usabilidad e investigación aplicada a interfaces",
        "orchestrator",
        ["product-manager", "product-designer", "tech-lead"],
        ["ui-designer", "ux-researcher", "ux-writer"],
        "open",
    ),
    (
        "ui-designer",
        "ui designer: sistemas visuales, componentes y consistencia de interfaz",
        "specialist",
        ["ux-designer", "product-designer", "frontend-developer"],
        [],
        "open",
    ),
    (
        "ux-researcher",
        "ux researcher: investigación con usuarios, hallazgos y evidencia para diseño",
        "specialist",
        ["ux-designer", "product-designer", "product-manager"],
        [],
        "open",
    ),
    (
        "ux-writer",
        "ux writer / content designer: microcopy, tono y claridad en productos digitales",
        "specialist",
        ["ux-designer", "product-designer", "ui-designer"],
        [],
        "open",
    ),
    # --- Engineering leadership ---
    (
        "software-architect",
        "software architect: boundaries, ADRs, trade-offs y arquitectura defendible",
        "orchestrator",
        ["product-manager", "tech-lead", "engineering-manager"],
        [
            "tech-lead",
            "backend-developer",
            "platform-engineer",
            "security-engineer",
            "devops-sre",
        ],
        "open",
    ),
    (
        "tech-lead",
        "tech lead: guía técnica del equipo, calidad de código y entrega",
        "orchestrator",
        ["software-architect", "engineering-manager", "product-manager"],
        [
            "backend-developer",
            "frontend-developer",
            "mobile-developer",
            "fullstack-developer",
            "code-reviewer",
            "qa-engineer",
            "devops-sre",
        ],
        "open",
    ),
    (
        "engineering-manager",
        "engineering manager: people management, capacidad del equipo y entrega predecible",
        "orchestrator",
        ["product-manager"],
        ["tech-lead", "scrum-master", "software-architect"],
        "open",
    ),
    # --- Engineering ICs ---
    (
        "backend-developer",
        "backend developer: APIs, servicios, datos y lógica de servidor robusta",
        "specialist",
        ["tech-lead", "software-architect", "fullstack-developer"],
        [],
        "open",
    ),
    (
        "frontend-developer",
        "frontend developer web: UI performante, accesible y alineada al design system",
        "specialist",
        ["tech-lead", "ui-designer", "fullstack-developer"],
        [],
        "open",
    ),
    (
        "mobile-developer",
        "mobile developer: apps iOS/Android nativas o multiplataforma de calidad producción",
        "specialist",
        ["tech-lead", "ui-designer", "product-designer"],
        [],
        "open",
    ),
    (
        "fullstack-developer",
        "fullstack developer: entrega vertical end-to-end con criterio de boundaries",
        "both",
        ["tech-lead", "product-owner"],
        ["backend-developer", "frontend-developer"],
        "open",
    ),
    (
        "platform-engineer",
        "platform engineer: plataformas internas, DX y golden paths para equipos",
        "specialist",
        ["software-architect", "tech-lead", "devops-sre"],
        [],
        "open",
    ),
    (
        "devops-sre",
        "devops / SRE: CI/CD, observabilidad, confiabilidad y operaciones",
        "specialist",
        ["tech-lead", "software-architect", "platform-engineer", "release-manager"],
        [],
        "open",
    ),
    (
        "data-engineer",
        "data engineer: pipelines, warehouses y datos confiables para analítica/ML",
        "specialist",
        ["software-architect", "tech-lead", "data-analyst", "ml-engineer"],
        [],
        "open",
    ),
    (
        "security-engineer",
        "security engineer AppSec: amenazas, controles y review de seguridad en el SDLC",
        "specialist",
        ["software-architect", "tech-lead", "devops-sre", "compliance-privacy"],
        [],
        "open",
    ),
    # --- Quality & process ---
    (
        "qa-engineer",
        "qa engineer / test engineer: estrategia de pruebas y calidad del producto",
        "orchestrator",
        ["tech-lead", "product-owner", "scrum-master"],
        ["automation-qa", "code-reviewer"],
        "open",
    ),
    (
        "automation-qa",
        "automation qa: suites automatizadas, CI de tests y señal confiable",
        "specialist",
        ["qa-engineer", "tech-lead", "devops-sre"],
        [],
        "open",
    ),
    (
        "scrum-master",
        "scrum master / agile coach: flujo, impedimentos y ceremonias efectivas",
        "specialist",
        ["product-manager", "engineering-manager", "tech-lead"],
        [],
        "open",
    ),
    (
        "code-reviewer",
        "code reviewer: reviews rigurosos de diff, riesgos y mantenibilidad",
        "specialist",
        ["tech-lead", "qa-engineer", "backend-developer", "frontend-developer"],
        [],
        "open",
    ),
    # --- Data ---
    (
        "data-analyst",
        "data analyst: métricas, experimentos y decisiones basadas en datos",
        "specialist",
        ["product-manager", "product-owner", "data-engineer"],
        [],
        "open",
    ),
    (
        "ml-engineer",
        "ml engineer / data scientist aplicado: modelos en producción con evaluación",
        "specialist",
        ["software-architect", "data-engineer", "tech-lead"],
        [],
        "open",
    ),
    # --- Adjacent ---
    (
        "technical-writer",
        "technical writer: documentación de producto/API clara y mantenible",
        "specialist",
        ["tech-lead", "software-architect", "product-manager"],
        [],
        "open",
    ),
    (
        "release-manager",
        "release manager: planes de release, riesgo y coordinación de despliegues",
        "specialist",
        ["tech-lead", "engineering-manager", "devops-sre", "qa-engineer"],
        [],
        "open",
    ),
    (
        "support-engineer",
        "support engineer L2/L3: diagnóstico, escalamiento y cierre de incidentes",
        "specialist",
        ["tech-lead", "devops-sre", "qa-engineer"],
        [],
        "open",
    ),
    (
        "compliance-privacy",
        "compliance / privacy specialist: requisitos regulatorios y privacidad en producto",
        "specialist",
        ["product-manager", "security-engineer", "software-architect"],
        [],
        "open",
    ),
]


def main() -> int:
    vault = find_vault()
    created = []
    failed = []
    for fid, brief, kind, by, invokes, mode in AGENTS:
        # skip if exact id already exists (do not clobber seed profiles)
        path = vault / "_META" / "forge" / "profiles" / f"{fid}.md"
        if path.is_file():
            created.append({"forge_id": fid, "skipped": True, "reason": "exists"})
            continue
        data = build_profile_from_brief(
            vault,
            brief,
            forge_id=fid,
            specialty=brief.split(":", 1)[-1].strip() if ":" in brief else brief,
            role_kind=kind,
            invocable_by_mode=mode,
            invocable_by=by,
            invokes=invokes,
            force=False,
        )
        if data.get("ok"):
            created.append(
                {
                    "forge_id": data["forge_id"],
                    "kind": kind,
                    "invokes": invokes,
                    "invocable_by": by,
                }
            )
        else:
            failed.append({"forge_id": fid, "error": data.get("error")})

    # catalog note
    catalog = vault / "_META" / "forge" / "catalog.md"
    if catalog.is_file():
        text = catalog.read_text(encoding="utf-8")
        marker = "## Agentes usuario — equipo software (draft)"
        if marker not in text:
            rows = [
                "| ID | kind | Nota |",
                "|----|------|------|",
            ]
            for fid, brief, kind, *_rest in AGENTS:
                rows.append(f"| `{fid}` | {kind} | draft Builder 2.0 — equipo software estándar |")
            block = (
                f"\n{marker}\n\n"
                "> Grafo **tuyos** (industria estándar). Semilla del repo sigue arriba. "
                "Completar corpus C1–C5 antes de `active`. Ver [[forge-delegation]].\n\n"
                + "\n".join(rows)
                + "\n"
            )
            catalog.write_text(text.rstrip() + "\n" + block, encoding="utf-8")

    print(f"ok={len([c for c in created if not c.get('skipped')])} skipped={len([c for c in created if c.get('skipped')])} failed={len(failed)}")
    for f in failed:
        print("FAIL", f)
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
