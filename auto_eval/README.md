# Auto Evaluation

Automated evaluation framework for TaskWeaver using a **Tester + Judge** architecture.

## Quick Start

1. Configure `taskweaver_config.json` under the `project` folder with your LLM endpoint.
2. Run a single case:
```bash
cd auto_eval
python taskweaver_eval.py -m single -p cases/echo
```
3. Run all cases:
```bash
python taskweaver_eval.py -m batch -p ./cases
```

## How It Works

### Tester
The Tester sends the `task_description` directly to the TaskWeaver agent as the first message. If the agent asks follow-up questions, an LLM generates responses grounded solely in the task description context. The conversation continues until the agent completes the task or `max_rounds` is reached.

### Judge
The Judge evaluates the conversation against each `scoring_point` using LLM-based judgment. For each criterion, the LLM determines whether it was met and provides a reason.

## Parameters

- `-m/--mode`: `single` or `batch`
- `-p/--path`: path to case directory (single) or parent directory (batch)
- `-r/--result`: result CSV file path (batch mode, default: `sample_case_results.csv`)
- `-f/--fresh`: re-evaluate all cases, ignoring previous results
- `-s/--sleep`: sleep time in seconds between evaluations (batch mode)

## Creating a Test Case

Create a directory under `cases/` with a single YAML file:

```yaml
version: 0.1
app_dir: ../project/
config_var:                            # Optional: TaskWeaver config overrides
  execution_service.kernel_mode: "local"
dependencies: []                       # Optional: Python packages to check
data_files: []                         # Optional: files to copy into session workspace
pre_command: []                        # Optional: shell commands to run before test
verbose: false                         # Optional: print internal agent posts
max_rounds: 10                         # Optional: max conversation rounds (default: 10)
task_description: |-
  Your task description here. This is sent directly to the agent.
scoring_points:
  - score_point: "Description of what should be true"
    weight: 1
  - score_point: "Another criterion"
    weight: 2
```

### Tips
- Write `task_description` as a direct instruction to the agent (it will be sent as-is).
- For multi-step tasks, list all steps in the task description. The tester will handle follow-up interactions.
- Each `scoring_point` is evaluated independently by the LLM judge.
- Use `weight` to indicate relative importance of each criterion.

## Architecture

```
auto_eval/
├── tester.py              # Tester: drives conversation with the agent
├── judge.py               # Judge: LLM-based scoring
├── prompts.py             # All prompt templates
├── taskweaver_eval.py     # Main entry point (single + batch)
├── utils.py               # load_task_case, check_package_version
├── README.md
└── cases/                 # Test case directories
```
