---
name: zamokctl
domain: development
source: "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\beshkenadze\\skills\\development\\zamokctl\\SKILL.md"
sources:
  - "C:\\Users\\david\\AppData\\Local\\hermes\\skills\\community\\beshkenadze\\skills\\development\\zamokctl\\SKILL.md"
tags: [development]
description: "Use when generating/managing the offline root signing key or signing & publishing Zamok product keysets from the terminal (the Swift CLI; the ZamokApp GUI is the co-equal interface). Triggers — \"generate root key\", \"rotate root\", \"publish keyset\", \"sign keyset\", \"escrow root key\", \"zamokctl\", \"trusted-roots.json\", Tish/Zamok license signature setup."
---

# zamokctl

**Dominio:** [[development]]  
**Fuente(s):**
- `C:\Users\david\AppData\Local\hermes\skills\community\beshkenadze\skills\development\zamokctl\SKILL.md`

**Descripción:** Use when generating/managing the offline root signing key or signing & publishing Zamok product keysets from the terminal (the Swift CLI; the ZamokApp GUI is the co-equal interface). Triggers — "generate root key", "rotate root", "publish keyset", "sign keyset", "escrow root key", "zamokctl", "trusted-roots.json", Tish/Zamok license signature setup.

**Cuándo usar:** `zamokctl` (Swift, target in `apps/macapp`) and the **ZamokApp GUI** are two thin interfaces over one shared `ZamokSigning` core. They share the **same root key in the macOS Keychain** and the same `/draft → confirm → verbatim-sign → /publish` flow. There is no bun/TS signing CLI

## Tags
#development

## Skills relacionadas
- [[biome]]
- [[codex-code-review]]
- [[dev-workflow]]
- [[git-worktree-workflow]]
- [[gitea-tea]]
- [[gitea-wiki]]
- [[ios-design-review]]
- [[ios-design-workflow]]
- [[ios-hig-reference]]
- [[ios-swiftui-generator]]
- [[omni-bench]]
- [[omni-bench-publish]]
- [[omni-bench-run]]
- [[python-uv]]
- [[research-guide]]
- [[swiftui-developer]]
- [[typescript-advanced-types]]
- [[zenstack]]
