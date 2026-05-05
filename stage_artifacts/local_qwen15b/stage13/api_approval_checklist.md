# Stage L13 Later API Approval Checklist

Use this checklist before any DeepSeek API request in a later approved stage.

## Must Be Approved Explicitly
- API call type: connectivity, single judge template, tiny batch, or larger batch
- Maximum request count
- Maximum examples judged
- Expected cost envelope
- Whether thinking/reasoning output is disabled
- Output path
- Logging policy

## Must Not Happen
- Print API keys
- Write API keys to files
- Modify `.env`
- Modify shell profiles
- Modify secret stores
- Run a full AlpacaEval-style evaluation without separate approval

## Allowed Before Approved API Call
- Presence check only, such as `DEEPSEEK_API_KEY present: yes`
- Static template/schema validation
- Synthetic local parser dry-run
