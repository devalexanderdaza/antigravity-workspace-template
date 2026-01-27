"""
Convenience entrypoint so `python agent.py` works from the repo root.

You can pass the task via CLI args or the AGENT_TASK env var.

Example:
    python agent.py 
"""
import os
import sys

from src.agent import GeminiAgent

def main():
    if len(sys.argv) == 1:
        task = os.environ.get("AGENT_TASK", "")
    else:
        task = " ".join(sys.argv[1:]).strip()

    print(f"Task: {task}")

    agent = GeminiAgent()
    try:
        agent.run(task)
    finally:
        agent.shutdown()

if __name__ == "__main__":
    main()