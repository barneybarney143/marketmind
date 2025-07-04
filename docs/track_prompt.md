# track_prompt.py

Small command line utility to record developer prompts for later analysis.
It appends metadata such as a complexity score, readability estimate and token
count to `logs/prompt_log.md`.

Typical invocation:

```bash
python track_prompt.py --prompt "Add unit tests" --session-id 123
```

### Options
- `--prompt` – text of the prompt to record (required)
- `--session-id` – unique session identifier
- `--project` – project name (default: `unknown`)
- `--file` – file name (default: `unknown`)
- `--log` – path to the log file
