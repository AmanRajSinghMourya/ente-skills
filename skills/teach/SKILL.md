---
name: teach
description: Teach Aman how a part of Ente works from the ground up, such as how the Go server sends emails end to end. Explains in controlled plain English (about 80% ASD-STE100), builds diagrams step by step, makes an interactive HTML page, and can render a 3Blue1Brown-style video with Manim. Use for /teach, "explain X from the ground up", "help me really understand X", or server code he's new to.
---

# Teach

Aman is a mobile engineer, strong in Dart and Flutter and new to backend. Teach
so he can predict what the code does before he opens it. For server questions,
read [references/museum.md](references/museum.md) first.

## Ground rules

- **Read the code first.** Every claim comes from a file you opened in this
  session, cited as `path/file.go:123`. Quote 3–10 lines, never whole
  functions. If you're unsure, check it or run it; never guess.
- **Assume no backend knowledge.** Never explain Dart or Flutter. Define every
  backend term at first use, in one clause. Never skip a step because it seems
  routine; a skipped step is where he gets lost.
- **Use Dart comparisons when they shorten things:** a Go struct is a class with
  only fields, `defer` is `finally`, `if err != nil` is try/catch spelled out.
- **Use real values:** "user 7 asks for a login code" beats "the user".
- No quizzes, no "next steps" or "focus areas", and no restating his question.

## Writing: about 80% ASD-STE100

ASD-STE100 (Simplified Technical English) is the controlled English of aircraft
manuals. Follow it most of the way:

- One idea per sentence. Keep sentences under about 20 words.
- Steps are numbered, with one action each.
- Active voice and present tense: "The controller sends the email", not "the
  email gets sent".
- One word for one thing. Pick a term, define it once, and never switch to a
  synonym (not "mailer", then "email service", then "sender").
- Common words. No idioms, no filler ("simply", "just", "basically").
- Say what the code shows, what you inferred, and what you didn't check.

## The ladder: do every level unless Aman asks for less

1. **Ground-up text, in the chat.**
   1. Base ideas first: the concepts the code rests on, each in two or three
      sentences with one everyday analogy. For example, for email: what SMTP
      is, what an email provider does, and what a template is.
   2. The map: which parts talk to which, in one short paragraph.
   3. The trace: the flow end to end, as numbered steps with real values and
      a `file:line` on each step.
   4. What can go wrong: failures, retries, limits.
   5. Where things live: a table of file and what it does.
   Bold the one sentence that is the core answer.
2. **Diagrams that build up.** For three or more parts, draw a series, not one
   big picture: first A to B, then the same diagram plus C, and so on. Label
   arrows with the real thing that moves (`POST /users/ott`,
   `INSERT INTO otts …`, `SMTP DATA`), and put file anchors under the boxes.
   Use Mermaid in the chat (Claude can also use inline visuals; Codex can use
   its `visualize` skill).
3. **Interactive HTML page.** One page that steps through the flow. Each
   "Next" highlights the next box in the diagram and shows that step's 1–3
   plain sentences and its quoted code with `file:line`. Add a glossary of the
   terms defined. Claude Code: publish it as an Artifact (load the
   `artifact-design` skill first). Codex: use the `visualize` skill or write
   one self-contained HTML file and open it.
4. **3Blue1Brown-style video,** made with Manim, 3Blue1Brown's own animation
   library.
   - Check `manim --version`. If Manim isn't installed, say so, give Aman the
     install steps, and stop. Never install it without his OK; AGENTS.md
     says to vet packages first.
   - Write `scene.py` in a scratch folder outside the repo: one scene per step
     of the trace, each building on the previous one, with boxes that appear,
     arrows that travel, and short on-screen captions in the same controlled
     English. Use `Text`, not `MathTex` (that needs LaTeX). Aim for 1–3
     minutes.
   - Render with `manim -qm scene.py <SceneName>`. Watch for errors, fix
     them, and send Aman the mp4 file.
