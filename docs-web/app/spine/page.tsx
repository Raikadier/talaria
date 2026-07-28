export default function Page() {
  return (
    <>
      <h1>SPINE</h1>
      <p className="lead">
        <em>Structured Protocol for Integrated Neural Execution</em> — antes
        IRONMAN. Coordina Ingest → Normalize → Orient → Retrieve → Memorize →
        Act → Notify.
      </p>
      <h2>Modos (Fase F)</h2>
      <ul>
        <li>
          <strong>strict</strong> — verify boot/close y gates FORGE obligatorios
          para declarar done.
        </li>
        <li>
          <strong>draft</strong> — exploración; no promete resultado
          garantizado.
        </li>
      </ul>
      <pre>{`skillgraph mode get --json
skillgraph mode set strict
skillgraph --mode draft verify boot --json`}</pre>
    </>
  );
}
