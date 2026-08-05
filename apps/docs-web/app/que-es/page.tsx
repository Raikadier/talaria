export default function Page() {
  return (
    <>
      <h1>Qué es Mímir</h1>
      <p className="lead">
        Mímir (mitología nórdica) custodia el pozo de la sabiduría.{" "}
        <strong>SkillGraph Cognitive Operating System (SGCOS)</strong> es la
        implementación técnica: un segundo cerebro operable por agentes.
      </p>
      <h2>Dos metáforas, un sistema</h2>
      <ul>
        <li>
          <strong>Hacia fuera:</strong> super-API de capacidades (
          <code>describe</code>, MCP, CLI).
        </li>
        <li>
          <strong>Hacia dentro:</strong> organismo con órganos (Memoria, AXON,
          FORGE, SPINE, Tools).
        </li>
      </ul>
      <h2>Principio rector</h2>
      <p>
        Una sola verdad: el vault Markdown. Chat/mem0 del agente = caché. Las
        tools son efectores, no cerebros rivales.
      </p>
      <h2>Nombres</h2>
      <table>
        <thead>
          <tr>
            <th>Uso</th>
            <th>Nombre</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Comercial</td>
            <td>Mímir</td>
          </tr>
          <tr>
            <td>Técnico</td>
            <td>SkillGraph Cognitive Operating System</td>
          </tr>
          <tr>
            <td>Acrónimo</td>
            <td>SGCOS</td>
          </tr>
          <tr>
            <td>Vault / repo</td>
            <td>SkillGraph</td>
          </tr>
        </tbody>
      </table>
    </>
  );
}
