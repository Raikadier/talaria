export default function Page() {
  return (
    <>
      <h1>Futuro</h1>
      <p className="lead">
        Mímir ya es operable. Estas son extensiones naturales del organismo.
      </p>
      <div className="grid">
        <div className="card">
          <h3>Eval LLM A/B</h3>
          <p>
            Correr baseline frontier vs FORGE+AXON automáticamente y publicar
            scorecards.
          </p>
        </div>
        <div className="card">
          <h3>engraph / Mk.4</h3>
          <p>Super-retrieval semántico sobre el vault sin segunda verdad.</p>
        </div>
        <div className="card">
          <h3>Más perfiles FORGE</h3>
          <p>
            Legal, finanzas, producto, sales — siempre vía builder + Leyes I/II.
          </p>
        </div>
        <div className="card">
          <h3>Marketplace de órganos</h3>
          <p>
            Packs instalables (skills + perfiles + evals) firmados para el
            vault.
          </p>
        </div>
        <div className="card">
          <h3>Multitenancy ligero</h3>
          <p>
            Varios vaults Mímir por equipo con sync selectivo de AXON/FORGE.
          </p>
        </div>
        <div className="card">
          <h3>UI Obsidian + web</h3>
          <p>
            Dashboard de verify/smoke/evals junto a esta documentación.
          </p>
        </div>
      </div>
    </>
  );
}
