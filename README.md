<h1 align="center">
    <img src="./.asset/logo.color.svg" width="45" /> TaskWeaver
</h1>

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3776AB?&logo=python&logoColor=white-blue&label=3.10%20%7C%203.11)&ensp;
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)&ensp;
![Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

</div>

TaskWeaver is a **code-first** agent framework for seamlessly planning and executing data analytics tasks. 
This innovative framework interprets user requests through code snippets and efficiently coordinates a variety 
of plugins in the form of functions to execute data analytics tasks in a stateful manner.

Unlike many agent frameworks that only track the chat history with LLMs in text, TaskWeaver preserves both the **chat history** and the **code execution history**, including the in-memory data. This feature enhances the *expressiveness* of the agent framework, making it ideal for processing complex data structures like high-dimensional tabular data.

<h1 align="center">
    <img src="./.asset/taskweaver_arch.png"/> 
</h1>

## Highlights

- **Planning for complex tasks** - Task decomposition and progress tracking for complex tasks
- **Reflective execution** - Reflect on execution and make adjustments
- **Rich data structures** - Work with Python data structures (DataFrames, etc.) instead of strings
- **Customized algorithms** - Encapsulate algorithms into plugins and orchestrate them
- **Domain-specific knowledge** - Incorporate domain knowledge to improve reliability
- **Stateful execution** - Consistent user experience with stateful code execution
- **Code verification** - Detect potential issues before execution
- **Easy to debug** - Detailed logs for LLM prompts, code generation, and execution

## Quick Start

### Step 1: Installation

TaskWeaver requires **Python >= 3.10**.

```bash
# Optional: create conda environment
conda create -n taskweaver python=3.10
conda activate taskweaver

# Clone and install
git clone https://github.com/microsoft/TaskWeaver.git
cd TaskWeaver
pip install -r requirements.txt
```

### Step 2: Configure the LLM

Configure `taskweaver_config.json` in your project folder:

```json
{
  "llm.api_key": "your-api-key",
  "llm.model": "gpt-4"
}
```

TaskWeaver supports OpenAI and Azure OpenAI APIs.

### Step 3: Run TaskWeaver

**Command Line (CLI):**
```bash
python -m taskweaver -p ./project/
```

**Web UI:**
```bash
python -m taskweaver -p ./project/ server --port 8000
# Open http://localhost:8000/chat in your browser
```

**As a Library:**
```python
from taskweaver.app.app import TaskWeaverApp

app = TaskWeaverApp(app_dir="./project/")
session = app.get_session()
response = session.send_message("Your request here")
```

## Documentation

- `AGENTS.md` - Development guide for AI agents and contributors
- `docs/` - Design documents and architecture details

## License

MIT License - see [LICENSE](LICENSE) for details.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
