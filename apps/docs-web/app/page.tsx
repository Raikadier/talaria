import Link from "next/link";

export default function HomePage() {
  return (
    <>
      <h1>El pozo de sabiduría para agentes</h1>
      <p className="lead">
        <strong>Mímir</strong> es la marca de{" "}
        <em>SkillGraph Cognitive Operating System</em> (SGCOS): un organismo +
        API para que cualquier piloto (Cursor, Hermes, Claude Code…) multiplique
        capacidad con memoria durable, skills enlazadas, roles elite y gates
        verificables.
      </p>
      <div className="hero-meta">
        <span className="chip">Comercial: Mímir</span>
        <span className="chip">Técnico: SGCOS</span>
        <span className="chip">Protocolo: SPINE</span>
        <span className="chip">CLI 1.0</span>
      </div>
      <Link className="cta" href="/quickstart">
        Empezar
      </Link>
      <Link className="cta secondary" href="/que-es">
        Leer el concepto
      </Link>

      <div className="grid">
        <div className="card">
          <h3>No es solo un MCP</h3>
          <p>
            Es estado canónico (vault), protocolo SPINE y órganos que no se
            pisan.
          </p>
        </div>
        <div className="card">
          <h3>Garantías en máquina</h3>
          <p>
            verify, forge check, axon search, eval harness y modos
            strict/draft.
          </p>
        </div>
        <div className="card">
          <h3>Cualquier agente</h3>
          <p>
            describe --json + MCP skillgraph/obsidian: descubrimiento sin
            folklore.
          </p>
        </div>
      </div>
    </>
  );
}
