NEEDS_RESPONSE_PROMPT = """\
You are analyzing an AI agent's response to determine if it is explicitly asking \
the user a question or requesting additional information before it can proceed.

The agent was given this task:
{task_description}

Reply with exactly one word:
- "yes" ONLY if the agent is explicitly asking a question or requesting specific \
information it needs to proceed (e.g., "What column should I use?", "Could you \
provide the file path?").
- "no" if the agent is reporting results, confirming task completion, providing \
an answer, or simply responding to the request. When in doubt, reply "no".

Do not explain your reasoning. Reply with only "yes" or "no".\
"""

TESTER_FOLLOW_UP_PROMPT = """\
You are a tester interacting with an AI agent. The agent is working on a task \
and has asked you a question. You must answer based ONLY on the information in \
the task description below. Do not invent information that is not in the task \
description.

## Task Description
{task_description}

## Instructions
- Answer the agent's question concisely using only information from the task description.
- If the task description does not contain the answer, say you don't have that \
information and ask the agent to proceed with reasonable defaults.
- Do not reveal scoring criteria or evaluation details.
- Keep your response short and direct.\
"""

JUDGE_PROMPT = """\
You are an evaluator judging whether an AI agent's conversation satisfies a \
specific scoring criterion.

You will be given:
1. The original task description
2. The full conversation between user and agent
3. A scoring criterion to evaluate

Evaluate whether the conversation demonstrates that the scoring criterion has \
been met. Consider the agent's responses, any code it executed, and any results \
it produced.

Reply in this exact JSON format:
{{
    "reason": "Brief explanation of why the criterion is or is not met",
    "is_hit": "yes or no"
}}

Reply ONLY with the JSON object. No other text.\
"""
