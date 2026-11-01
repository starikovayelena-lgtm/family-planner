# Family planner

Yelena's Claude setup for family birthdays and travel. Private repo.

- `.claude/agents/birthday-planner.md`: the birthday agent (Claude Code)
- `.claude/skills/birthday-planner/`: birthday know-how, family memory (`references/family.md`), templates, tracker script
- `.claude/skills/yelena-travel/`: family travel planner
- `birthdays/<child>-<year>/`: each party's plan and tracker

## Use it
Start a Claude Code session on this repo and say e.g. "Amelia fyller 9 i mars, hjälp mig med kalaset", or "use the birthday-planner agent".
After each party, say "log this year" so the birthday log in `references/family.md` is updated and committed.
