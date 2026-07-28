export default function Page() {
  return (
    <>
      <h1>Garantías A–F</h1>
      <p className="lead">
        De “documentado” a “fallible en máquina”. Sin gates ejecutables no hay
        garantía — solo recomendación.
      </p>
      <table>
        <thead>
          <tr>
            <th>Fase</th>
            <th>Entrega</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>A</td>
            <td>verify boot/close + scorecard</td>
            <td>Hecho</td>
          </tr>
          <tr>
            <td>B</td>
            <td>doctor organismo + smoke</td>
            <td>Hecho</td>
          </tr>
          <tr>
            <td>C</td>
            <td>forge list/show/check/run</td>
            <td>Hecho</td>
          </tr>
          <tr>
            <td>D</td>
            <td>axon search + queries</td>
            <td>Hecho</td>
          </tr>
          <tr>
            <td>E</td>
            <td>eval harness (5 gold)</td>
            <td>Hecho</td>
          </tr>
          <tr>
            <td>F</td>
            <td>modos strict/draft</td>
            <td>Hecho</td>
          </tr>
        </tbody>
      </table>
      <pre>{`skillgraph smoke --json
skillgraph eval list --json
skillgraph eval run research-brief --deliverable _META/evals/fixtures/research-brief-pass.md --json`}</pre>
    </>
  );
}
