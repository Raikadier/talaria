export default function Page() {
  return (
    <>
      <h1>AXON</h1>
      <p className="lead">
        <em>Ability Crosslink & Operational Network</em> — el grafo de skills
        listo para Retrieve.
      </p>
      <pre>{`skillgraph axon search "refactor testing" --json
skillgraph axon for-profile researcher --json
skillgraph axon stats --json`}</pre>
      <p>
        Los perfiles FORGE declaran <code>axon_queries</code> para enrutar
        Retrieve sin improvisar.
      </p>
    </>
  );
}
