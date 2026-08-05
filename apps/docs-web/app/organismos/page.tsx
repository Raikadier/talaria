export default function Page() {
  return (
    <>
      <h1>Órganos</h1>
      <p className="lead">
        Cada órgano tiene una función vital. Ninguno es un producto aparte.
      </p>
      <table>
        <thead>
          <tr>
            <th>Órgano</th>
            <th>Función</th>
            <th>Ubicación</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Memoria</td>
            <td>Episodios, decisiones, proyectos</td>
            <td>
              <code>memory/</code>
            </td>
          </tr>
          <tr>
            <td>AXON</td>
            <td>Skills interconectadas</td>
            <td>
              <code>skills/</code>
            </td>
          </tr>
          <tr>
            <td>FORGE</td>
            <td>Perfiles de rol elite</td>
            <td>
              <code>_META/forge/</code>
            </td>
          </tr>
          <tr>
            <td>SPINE</td>
            <td>Protocolo / sistema nervioso</td>
            <td>
              <code>_META/spine-framework.md</code>
            </td>
          </tr>
          <tr>
            <td>API</td>
            <td>CLI + MCP</td>
            <td>
              <code>skillgraph_cli/</code>
            </td>
          </tr>
          <tr>
            <td>Tools</td>
            <td>Ingest y actuación</td>
            <td>
              <code>tools/</code>
            </td>
          </tr>
        </tbody>
      </table>
    </>
  );
}
