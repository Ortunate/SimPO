# Local Hardware Notes

The local machine is for development and validation only.

Codex must not modify WSL, CUDA, NVIDIA driver, or global environment settings without human approval.

If WSL memory is insufficient, Codex may suggest a `.wslconfig` change, but must not apply it automatically.

Example WSL2 memory configuration, to be reviewed by the human supervisor before use:

    [wsl2]
    memory=48GB
    swap=16GB
    processors=12

After editing `.wslconfig`, WSL must be restarted from PowerShell:

    wsl --shutdown

The exact values must be chosen by the human supervisor based on available host RAM and current workload.
