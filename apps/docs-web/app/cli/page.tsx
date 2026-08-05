export default function Page() {
  return (
    <>
      <h1>CLI & MCP</h1>
      <p className="lead">
        La superficie API del organismo. Los agentes descubren el cuerpo con{" "}
        <code>describe --json</code>.
      </p>
      <pre>{`pip install -e .
python -m skillgraph_cli describe --json
python -m skillgraph_cli connect --client cursor --json
python -m skillgraph_cli mcp`}</pre>
      <h2>MCP</h2>
      <ul>
        <li>
          <code>skillgraph</code> — orquestación (doctor, verify, forge, axon,
          ingest…)
        </li>
        <li>
          <code>obsidian</code> — CRUD de notas del vault
        </li>
      </ul>
    </>
  );
}
