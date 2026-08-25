# SCENDO — Agent Instructions

## Diagrams

All diagrams must be **Mermaid diagrams**.

**File organisation:**
- Source: `.mmd` file (e.g., `docs/diagrams/process-overview.mmd`)
- Rendered: `.png` alongside it (e.g., `docs/diagrams/process-overview.png`)
- Markdown documents embed the **PNG**, never raw MMD syntax inline

**Rendering — always 3× scale for legibility:**
```bash
mmdc -i docs/diagrams/<name>.mmd -o docs/diagrams/<name>.png -s 3 --backgroundColor white
```

**Diagram quality rules:**
- Choose layout direction (`LR`, `TB`, `BT`) for the specific diagram — don't default blindly to top-down
- Group related nodes; use subgraphs to reduce visual clutter
- Keep labels short enough to read at the rendered size; break long labels with `<br/>`
- After rendering, visually check the PNG at 100% zoom — small text must be legible without zooming in

**Checklist for every new/updated diagram:**
1. Edit or create the `.mmd` source file under `docs/diagrams/`
2. Run `mmdc` at `-s 3` to regenerate the PNG
3. Visually verify the PNG — check label legibility and layout
4. Embed the PNG in the relevant markdown doc with a relative path: `![alt text](diagrams/<name>.png)`
5. Commit both `.mmd` and `.png`
