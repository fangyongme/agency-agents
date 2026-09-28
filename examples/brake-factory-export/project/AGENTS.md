# Brake factory export project

Read `OPERATING-RULES.md`, then `RUNBOOK.md` and the current
`knowledge/factory-profile.json`. Use only the files relevant to the current
stage. Start each run by reading `work/pipeline.json` and existing campaign
outputs; resume completed work rather than recreating it.

The main Codex session coordinates four project custom agents:

| Agent name | Stage | Primary output |
| --- | --- | --- |
| Outbound Strategist | Research, then B2B qualification | research.md; qualification.json |
| Social Media Strategist | Master brief, LinkedIn, content review | content-brief.md; linkedin.md; review.md |
| Video Optimization Specialist | TikTok / Instagram / YouTube assets | video-pack.md |
| Sales Outreach | First contact, replies, RFQ follow-up | outreach/*.md; rfq/*.json |

Keep dependent stages ordered. Read returned artifacts before handing them to
the next role. Independent LinkedIn/video production can overlap after the
brief exists, but they must write different files. Do not activate the full
agency roster or add more agents for a task these four cover. If custom-agent
spawning is unavailable, execute each role sequentially using the installed
`.codex/agents/<slug>.toml` instructions and state that this was a single-session
fallback. Do not pretend multiple agents ran.

Only the coordinator writes `work/pipeline.json`, assigns stable IDs, reconciles
duplicates, checks external-action authorization and reports completion. Each
handoff states input paths/revisions, output paths, evidence, blockers, status,
next owner and next action. Never advance a stage on an incomplete handoff.

For setup without actual factory facts, complete research plans and production
briefs, list missing evidence and ask only for the input blocking the next step.
The template is not a verified product catalog or a record of work already done.
