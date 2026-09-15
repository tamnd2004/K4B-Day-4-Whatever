# Tool Calling Mental Model & Lab Scope Established

Established the mental model of LLM tool-calling (schema declaration, model parameter emission, local python function dispatch) and grounded the project scope to the IT Helpdesk domain with OpenRouter. Defined the 6 core failure modes evaluated by `run_eval.py` (`wrong_tool`, `wrong_arg_value`, `missing_info`, `wrong_boundary`, `unnecessary_tool`, `out_of_scope`), establishing that the assignment focuses on iterative artifact refinement (`system_prompt.md` and `tools.yaml`) rather than rebuilding the agent execution engine.
