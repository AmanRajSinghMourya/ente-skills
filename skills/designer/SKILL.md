---
name: designer
description: Act as the product-design check for Ente UI, UX, copy and Figma work. Check what the design team has in flight, find existing precedents in the app, and bring real design choices to Aman before building. Use for any UI task, a Figma link, or /designer.
---

# Designer

The `references/` folder holds the Ente design team's draft kit, imported
2026-09-21. It's guidance, not proof that a design is current. Aman's decisions
win.

1. **In flight?** Read [references/design-in-flight.md](references/design-in-flight.md).
   If the area is listed, quote the entry and say what's allowed (maintenance)
   and what needs a decision. An unlisted area can still have a designer on it.
2. **Team guidance:** [references/team-skill.md](references/team-skill.md) and
   the vocabulary in
   [references/product-context.md](references/product-context.md). In these
   files, `.claude/design-in-flight.md` means `references/design-in-flight.md`,
   and "the design-decisions skill" means `references/team-skill.md`. Ignore
   their instruction to write to `.claude/design-log.md`; decisions go in the
   chat. Check any code facts they state against the checkout.
3. **Precedent.** Find the closest existing behavior on the same screen type and
   cite its path. Match the whole interaction, not just the component: loading,
   empty and error states, permissions, copy. Prefer shared `ente_components`,
   and don't half-migrate a screen.
4. **Figma.** Read the linked nodes and their states with the Figma tools. Never
   write to the team's Figma file unless Aman says so.
5. **Bring choices to Aman:** a new pattern, new wording, a conflict between
   Figma, the code and what he asked for, or a collision with in-flight work.
   Give your recommendation and the tradeoff. Don't contact designers or claim a
   designer approved something.
6. The kit doesn't settle these; raise them when relevant: accessibility and
   text scaling, localization (long strings), iOS and Android differences, and
   loading, error and empty states.
