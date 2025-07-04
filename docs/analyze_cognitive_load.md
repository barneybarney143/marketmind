# analyze_cognitive_load.py

Parses `logs/prompt_log.md` produced by `track_prompt.py` and checks for
potential cognitive overload situations. It reads optional thresholds from
`tracker_config.yaml` and touches `.you-need-a-break` when the limits are
exceeded.

## Functions
- `parse_logs(path)` – return a list of `PromptEntry` records from the markdown log
- `load_config()` – load limit values from `tracker_config.yaml`
- `analyze(entries, config)` – apply heuristics and return `True` when overload
  is detected

Running the script exits with code 1 and prints a warning when overload is
found.
