from __future__ import annotations

from talaria_cli.mcp_server import TOOLS, TalariaMCP
from talaria_cli.vault import find_vault


REQUIRED = {
    "talaria_describe",
    "talaria_connect",
    "talaria_session_start",
    "talaria_session_status",
    "talaria_session_close",
    "talaria_mode_get",
    "talaria_mode_set",
    "talaria_axon_feedback",
    "talaria_axon_quality",
    "talaria_eval_list",
    "talaria_eval_show",
    "talaria_eval_run",
    "talaria_forge_run",
    "talaria_forge_build",
    "talaria_forge_invoke",
    "talaria_forge_graph",
    "talaria_verify_boot",
}


def test_mcp_tools_registered():
    names = {t["name"] for t in TOOLS}
    missing = REQUIRED - names
    assert not missing, f"missing MCP tools: {missing}"
    assert "talaria_describe" in names


def test_mcp_describe_and_connect_and_session_status():
    vault = find_vault()
    mcp = TalariaMCP(vault)
    desc = mcp.call("talaria_describe")
    assert desc.get("name") == "talaria"
    tools = desc.get("mcp", {}).get("tools") or []
    assert "talaria_session_start" in tools
    assert "talaria_connect" in tools

    conn = mcp.call("talaria_connect", {"client": "cursor"})
    assert conn.get("ok") is True
    assert "mcpServers_fragment" in conn

    dry = mcp.call("talaria_connect", {"client": "cursor", "apply": True, "confirm": False})
    assert dry.get("ok") is False

    st = mcp.call("talaria_session_status")
    assert "active" in st

    mode = mcp.call("talaria_mode_get")
    assert mode.get("mode") in {"strict", "draft"}
