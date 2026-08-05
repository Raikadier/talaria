export default function Page() {
  return (
    <>
      <h1>FORGE</h1>
      <p className="lead">
        <em>Framework for Operational Role Generation & Excellence</em>. Perfiles
        con Ley I (efectividad total) y Ley II (superior a modelo potente).
      </p>
      <pre>{`skillgraph forge list --ensembles --json
skillgraph forge run researcher --with-axon --json
skillgraph forge check --profile researcher --deliverable note.md --json`}</pre>
      <h2>Perfiles semilla</h2>
      <p>researcher · social-advisor · sw-architect · sw-engineer · programmer</p>
      <p>Ensemble: software-triad (Architect → Engineer → Programmer).</p>
    </>
  );
}
