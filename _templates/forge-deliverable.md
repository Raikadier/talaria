---
date: {{date}}
type: forge-deliverable
forge_profile: "{{profile}}"
forge_gates:
  G1: pass
  G2: pass
  G3: pass
tags: [forge, deliverable]
status: draft
---

# FORGE deliverable — {{profile}}

Declare each gate as `pass` / `fail` / `n/a` in frontmatter `forge_gates` (or lines `G1: pass` in body).

Then:
```bash
skillgraph forge check --profile {{profile}} --deliverable <this-file> --json
```
