# AGENTS.md

This file defines the AI agents used in the Codex-powered development workflow. Each agent is responsible for a specific role in the software development lifecycle. Click on the links to view their detailed instruction files.

## PromptRouterAgent

### Role
Monitors incoming prompts and decides which agent(s) should be invoked based on intent, scope, and structure.

### Input
- A single user prompt
- Optional metadata (timestamp, file, project context)

### Output
- Agent invocation plan (e.g. `[PlannerAgent] → [CoderAgent] → [TestAgent]`)
- Justification for each agent involved
- Task routing plan in `router_plan.yaml`

### Decision Process
- If the prompt contains **"build", "create", "implement"** → route to `PlannerAgent`
- If the prompt is a **system breakdown or feature** → `PlannerAgent` → `CoderAgent`
- If it includes **"test", "coverage", "cases"** → `TestAgent`
- If it includes **"review", "issues", "slow", "correct"** → `AuditAgent`
- If it includes **"document", "docs", "explain"** → `DocAgent`
- If it includes **"clean up", "simplify", "refactor"** → `RefactorAgent`

### Constraints
- Max 3 agents per plan unless overridden
- Must log all routing plans to `logs/prompt_log.md`
- Must avoid redundant agent invocation

### Output Example

```yaml
prompt: "I need to add a new caching mechanism to reduce DB load"
agents_called:
  - PlannerAgent
  - CoderAgent
  - TestAgent
reasoning: >
  The prompt describes a feature involving implementation and performance.
  Planning is required before writing code. Testing is necessary to verify behavior.
```

## Agent Directory

| Agent           | Role Description                                           | Instruction File                  |
|-----------------|------------------------------------------------------------|-----------------------------------|
| PlannerAgent    | Decomposes high-level features into concrete tasks         | [PlannerAgent](agents/PlannerAgent.md) |
| CoderAgent      | Implements components based on task definitions            | [CoderAgent](agents/CoderAgent.md)     |
| TestAgent       | Generates test cases for implemented components            | [TestAgent](agents/TestAgent.md)       |
| AuditAgent      | Reviews code for correctness and style                     | [AuditAgent](agents/AuditAgent.md)     |
| DocAgent        | Documents the codebase and API behavior                    | [DocAgent](agents/DocAgent.md)         |
| RefactorAgent   | Improves structure and readability without changing logic  | [RefactorAgent](agents/RefactorAgent.md) |

## Usage Guidelines

- Refer to this file when invoking agents in prompts.
- Use consistent input formats and clearly scoped tasks.
- Review agent output and feed results into the next stage when chaining agents. 

# Coding and Testing Standards

This project follows strict linting and typing rules. The main tools are:

- **Ruff** for linting (configured in `pyproject.toml`)
- **mypy** for static type checking
- **pytest** for testing

All code must pass Ruff, mypy, and pytest locally before being committed. Continuous integration runs these tools on every push and pull request to `main`.

Consider the instructions in SYSTEM.md!

## Project Index
- [README](README.md)
- [Strategy Descriptions](docs/strategies.md)
