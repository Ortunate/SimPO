# API Evaluation Policy

## Scope
DeepSeek V4 Flash may be used later as an AlpacaEval-style judge for the local fallback line.

Credential setup and encrypted key management are out of scope for this Codex conversation line.

## Hard Restrictions
Codex must not:

- configure API keys
- store API keys
- decrypt API keys
- print secret values
- write keys to files
- modify shell profiles
- modify secret stores
- run full API evaluation without explicit approval

## Allowed Before Approved API Calls
Before a future approved API call, Codex may only check whether required key/config variables exist.

Presence checks must not print secret values. Acceptable output examples:

- `DEEPSEEK_API_KEY present: yes`
- `DEEPSEEK_API_KEY present: no`

Do not echo, log, serialize, or persist the value.

## Approval Required
Ask for explicit approval before:

- any real API request
- any judge-template connectivity test
- any batch evaluation
- any cost-incurring API usage
- any AlpacaEval-style run

## Evaluation Staging
Recommended later sequence:

1. Static judge template validation with no API call.
2. Approved single-request connectivity test using non-sensitive output.
3. Approved tiny judge run on a few examples.
4. Approved local fallback comparison report.

Full AlpacaEval-style evaluation is a separate approval gate.
