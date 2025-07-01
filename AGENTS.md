# AGENTS.md

This file defines the AI agents used in the Codex-powered development workflow. Each agent is responsible for a specific role in the software development lifecycle. Click on the links to view their detailed instruction files.

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
