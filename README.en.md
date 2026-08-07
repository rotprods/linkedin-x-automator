# LinkedIn · X Automator

**An AI agent engine that posts for you on X (Twitter) and LinkedIn, autonomously.** It researches every 4 hours, scores viral signals, writes the copy, generates the image, posts on its own, measures and learns from results. From **0 to 100,000 followers**.

> 🎓 **For students:** this repo is a **self-installation kit**. You only need to paste ONE prompt into your Higgsfield Supercomputer and the agent handles the onboarding, installation and step-by-step setup.

---

## 🚀 Quick start in 3 steps (for students)

### 1. Create your Higgsfield account
Go to [higgsfield.ai](https://higgsfield.ai) and open **Supercomputer** ("Automation, skills, apps and more").

### 2. Clone or upload this repo to your Supercomputer
```
git clone https://github.com/rotprods/linkedin-x-automator.git
```
(Or upload it directly from your Supercomputer if you don't use git.)

### 3. Paste PROMPT-0
Open a chat in your Supercomputer and paste the contents of **[`PROMPT-0-ARRANQUE.md`](PROMPT-0-ARRANQUE.md)**.

The agent runs a **9-question onboarding**, installs the skills and subagents, guides you through Slack setup and connecting your networks, schedules the crons, runs a **dry-run test**, and only posts after you give the **GO**.

---

## 📦 What's included

| Path | Content |
|---|---|
| `PROMPT-0-ARRANQUE.md` | The single prompt you paste to install everything |
| `PROMPTS-1-9.md` | Per-phase booster prompts |
| `skills/` | The 4 engine skills (templates) |
| `agents/` | The subagent team (templates) |
| `config/` | Config templates (platforms, cadence, topics, secrets) |
| `onboarding/` | Step-by-step guides (Slack, connectors, checklist, questionnaire, FAQ) |
| `data/schema.sql` | SQLite schema (no data) |
| `tests/` | End-to-end repo test |

## 🧠 How it works (in simple terms)

1. **Researches** every 4h → viral signals with real sources.
2. **Scores** 0-100 and picks the best.
3. **Generates** a 16:9 image + copy (X in English, LinkedIn in Spanish).
4. **Queues** → **posts** within your best-hours.
5. **Measures** and **learns**: re-weights topics by engagement.

## 🧪 Repo test
Validate the kit is complete and has no personal data:
```bash
python3 tests/e2e/test_repo.py
```
Checks: structure, sanitization (0 personal data), config placeholders, SQLite schema, and that PROMPT-0 is complete.

## 🛡️ Security
- **Kill-switch:** `auto_publish: false` by default → the engine only queues, never posts until YOU give the GO.
- **Your credentials** (webhooks, chatId, tokens) go in `config/secrets.env` (gitignored) — **never in the public repo**.
- **Real sources** with verifiable URLs. Nothing invented.

## ⚙️ Stack
- Python 3.11 + SQLite · Higgsfield Supercomputer (skills, agents, connectors, crons)
- OAuth publishing (X + LinkedIn) · Slack/Telegram alerts

## 📄 License
MIT — free for educational and personal use.

> **Questions?** Check `onboarding/checklist-final.md` and `onboarding/cuestionario-9-preguntas.md` first. The agent guides you through the whole process.