# Mission: IT Helpdesk Tool-Calling AI Agent (Day 04 Lab)

## Why
Successfully build, evaluate, and deliver a production-ready IT Helpdesk AI Assistant for the VinUni AIA Day 04 lab. Mastering prompt engineering and tool calling will enable building reliable LLM systems that follow strict business policies, execute deterministic tool calls, and protect sensitive enterprise data.

## Success looks like
- Understand the complete LLM tool-calling lifecycle: prompt & tool schema declaration -> provider routing -> function dispatch -> evidence synthesis.
- Execute baseline evaluation (`v0`) with OpenRouter and diagnose concrete failure modes (`wrong_tool`, `wrong_arg_value`, `missing_info`, `wrong_boundary`).
- Implement hypothesis-driven iterations across `v1`, `v2`, and `v3` by refining `system_prompt.md` and `tools.yaml`, logging results in `version_log.csv`.
- Design and evaluate 10 custom team evaluation test cases (5 single-turn and 5 multi-turn) in `data/eval_group.json`.
- Pass 12 adversarial safety checks ensuring zero data exfiltration, strict identity confirmation before ticket creation, and policy compliance.
- Run a functioning chat UI displaying live tool calls, inputs, and outputs/errors, and complete `REPORT.md` and `TEAM.md` for final submission.

## Constraints
- Domain: IT Helpdesk (Northstar Labs internal service desk).
- LLM Provider: OpenRouter API.
- Team: 4 members on repository `tamnd2004/K4B-Day-4-Whatever`.
- Learning approach: Conceptual walkthrough and mental models first, followed by hands-on execution.

## Out of scope
- Switching to a non-IT custom domain (e.g. Travel, Library) which requires drafting 42 new test cases before v0.
- Model fine-tuning or training from scratch.
- Full backend re-writes beyond the specified agent loop and tools.
