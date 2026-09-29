# Start the four-agent project

1. Open this directory as a Codex project and start a new session. Project
   custom agents are in `.codex/agents/`; no global installation is needed.
2. Edit private `knowledge/factory-profile.json` with verified factory details.
   Keep catalogs, footage, quotes and customer files under ignored `work/` and
   reference their paths in the profile. Do not commit operational data.
3. Use the prompts in `RUNBOOK.md`. You can begin with research and draft asset
   requests while product-specific evidence is missing.
4. Check `work/pipeline.json` and campaign outputs on each run. Content drafts,
   actual media files, publication receipts and delivered messages are separate.

These files configure roles and handoffs. They do not connect social accounts,
render video without tools, send messages, schedule recurring work or provide
factory prices. Add those capabilities only when actually needed and authorized.
If native custom agents are unavailable, use the sequential fallback in AGENTS.md.

See `SOURCE-MANIFEST.json` for the exact source paths and hashes used at setup.
For an updated preset, generate a fresh sibling project and review its diff;
setup deliberately refuses to overwrite an existing edited instruction file.
