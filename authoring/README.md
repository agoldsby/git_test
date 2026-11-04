# Authoring guide — AI Tutorial: Basics

This folder is for people who **maintain** the course. Learners never see it; they get
only the `ai-tutorial-basics/` folder (zipped as `dist/ai-tutorial-basics.zip`).

## How the course works

Chat apps (Claude, ChatGPT) accept **files**, not folders, and don't remember earlier chats.
So the course is built around a single file:

| Original (Claude Code CLI) | This version (chat apps) |
|---|---|
| `CLAUDE.md` per module, loaded by `/start-1-1`, `/start-1-2` | One `COURSE.md` with every module; the learner drags it in and types **start** |
| Claude reads files with `@file` / `ls` | The learner **uploads** files into the chat (the skill being taught) |
| Claude edits files on disk (`feedback-synthesis.md`, etc.) | Results appear in the chat (or an artifact / canvas); later scenarios build on earlier chat context |
| Hidden `.progress` file + `/resume` | **Save codes** (`RELAY-1.2-S3`) the learner types as `resume CODE` in a new chat |
| `jira-progress-tracker` / `jira-feedback-logger` skills | Removed (no tool access in chat apps) |
| `/help` slash command | Learner types **help** (or `/help`) |

`COURSE.md` has three parts:
1. **Tutor Operating Rules.** These tell the AI how to behave: how to start, the Say / Check / Do
   conventions, learner commands, how to fit Claude vs. ChatGPT, save codes, resume.
2. **Reference Material.** The folder map, the company-context files (copied in at build
   time), and **answer keys** that tell the tutor what a strong result looks like.
3. **Module Scripts.** Module 1.1 (Welcome & Orientation) and Module 1.2 (First Tasks:
   five scenarios).

## Editing

Don't edit `ai-tutorial-basics/COURSE.md` directly. It's generated. Edit the sources:

| To change… | Edit |
|---|---|
| Tutor behavior, commands, save codes | `src/00-tutor-engine.md` |
| What a "good answer" looks like for each scenario | `src/05-answer-keys.md` |
| Module 1.1 script | `src/10-module-1.1.md` |
| Module 1.2 script | `src/20-module-1.2.md` |
| The end-of-file reminder | `src/90-closing-reminder.md` |
| Relay company background | `ai-tutorial-basics/practice-files/company-context/*.txt` (copied into COURSE.md automatically) |
| Practice files | `ai-tutorial-basics/practice-files/module-1.2-first-tasks/` (also update the answer keys!) |

Then rebuild from the repository root:

```bash
python3 authoring/build.py
```

That rewrites `ai-tutorial-basics/COURSE.md` and `dist/ai-tutorial-basics.zip`.

**Adding a module:** create `src/30-module-1.3.md` (files are joined in name order, and
`90-closing-reminder.md` stays last). Add it to the course map and the save-code table in
`00-tutor-engine.md`, and to the folder map if it has practice files.

### Script conventions

- **Say:** text the tutor sends nearly word-for-word.
- **Check:** the tutor stops and waits for the learner.
- **Do:** work the tutor does without narrating it.
- **Expected result** / answer keys: guidance for generating real output, not text to recite.
- **📌 SAVE POINT:** the tutor shows a save code here.

Keep the exact phrase you want the learner to type in **bold** (for example **Tell me about Relay**).

### The dashboard image

`practice-files/module-1.2-first-tasks/dashboard-example.png` was rendered from an HTML
mock-up. Its numbers have to match `COMPANY.txt`, `05-lena-ortiz-data.txt`, and the Scenario 4
answer key: completion 65% vs. an 80% target; Day-30 retention 71% → 62%; sign-ups +40%
(7,480 in Q2); funnel 100/95/88/69/65; setup tickets 38%.

## Testing checklist

Before sharing a new version, run through it once in **each** of:
- [ ] Claude (claude.ai or desktop), free and paid if possible
- [ ] ChatGPT (chatgpt.com or desktop), free and paid if possible

Check that:
- [ ] Typing **start** begins Module 1.1 Step 1 right away (no "I've reviewed the file…")
- [ ] The tutor stops at every Check instead of running ahead
- [ ] Uploading 8 files at once works (Scenario 2)
- [ ] The image is read correctly (Scenario 4)
- [ ] Web search on and off are both handled (Scenario 5)
- [ ] `help`, `where am I`, and `resume RELAY-1.2-S3` in a fresh chat all work
- [ ] The tutor never mentions "the script" or the course file's instructions
