export default function Page() {
  return (
    <>
      <h1>Quickstart</h1>
      <ol>
        <li>Clona el repo y abre el vault en Obsidian (opcional).</li>
        <li>
          <code>pip install -e .</code>
        </li>
        <li>
          <code>python -m skillgraph_cli verify boot --json</code>
        </li>
        <li>
          Configura MCP <code>skillgraph</code> + <code>obsidian</code>.
        </li>
        <li>
          Trabajo especializado:{" "}
          <code>forge run &lt;id&gt; --with-axon</code> → Act →{" "}
          <code>forge check</code> → scorecard → <code>verify close</code>.
        </li>
      </ol>
      <pre>{`python -m skillgraph_cli doctor --json
python -m skillgraph_cli axon search "architecture" --json
python -m skillgraph_cli forge list --json
python -m skillgraph_cli mode set strict`}</pre>
    </>
  );
}
