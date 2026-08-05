from __future__ import annotations

from pathlib import Path

from talaria_cli.util import EXIT_ERROR, EXIT_OK, EXIT_USAGE, emit, run_python_script


def run_ingest_doc(vault: Path, source: str, output: str | None = None, *, as_json: bool = False) -> int:
    script = vault / "_tools" / "ingest_document.py"
    if not script.is_file():
        emit({"error": "ingest_document.py missing"}, as_json)
        return EXIT_ERROR
    args = [source]
    if output:
        args.extend(["-o", output])
    code = run_python_script(script, args)
    if as_json:
        emit({"command": "ingest.doc", "source": source, "exit": code}, True)
    return EXIT_OK if code == 0 else EXIT_ERROR


def run_ingest_project(
    vault: Path, project: str, name: str | None = None, *, as_json: bool = False
) -> int:
    script = vault / "_tools" / "ingest_project.py"
    if not script.is_file():
        emit({"error": "ingest_project.py missing"}, as_json)
        return EXIT_ERROR
    args = [project]
    if name:
        args.extend(["--name", name])
    code = run_python_script(script, args)
    if as_json:
        emit({"command": "ingest.project", "project": project, "exit": code}, True)
    return EXIT_OK if code == 0 else EXIT_ERROR


def run_ingest(vault: Path, kind: str, target: str | None, **kwargs) -> int:
    if not target:
        emit({"error": "missing target path/url"}, kwargs.get("as_json", False))
        return EXIT_USAGE
    if kind == "doc":
        return run_ingest_doc(vault, target, kwargs.get("output"), as_json=kwargs.get("as_json", False))
    if kind == "project":
        return run_ingest_project(vault, target, kwargs.get("name"), as_json=kwargs.get("as_json", False))
    emit({"error": f"unknown ingest kind: {kind}"}, kwargs.get("as_json", False))
    return EXIT_USAGE
