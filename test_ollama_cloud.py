"""Quick smoke test: sends one request to Ollama cloud via resolve_model.

Run from the repo root:
    uv run python test_ollama_cloud.py

OLLAMA_API_KEY must be set in .env before running.
"""

# truststore must be injected before any SSL context is created.
# It makes Python use the macOS Keychain (which already trusts corporate/proxy
# CA certs), so the same certificates the browser trusts work here too.
import truststore
truststore.inject_into_ssl()

import asyncio
import os

from observability.instrument import load_env

load_env()  # reads .env into os.environ (existing env vars win)

from agents import Agent, Runner, RunConfig

from agent.agent import resolve_model

OLLAMA_MODEL = "gemma4:31b"


async def main() -> None:
    key = os.environ.get("OLLAMA_API_KEY", "")
    if not key:
        raise SystemExit(
            "OLLAMA_API_KEY is not set.\n"
            "Add it to .env:  OLLAMA_API_KEY=your-key-here\n"
            "Create a key at: https://ollama.com/settings/keys"
        )

    model = resolve_model(OLLAMA_MODEL)
    agent = Agent(
        name="ollama-smoke-test",
        instructions="You are a brief test assistant.",
        model=model,
    )

    result = await Runner.run(
        agent,
        'Reply with exactly: "Ollama cloud is working."',
        run_config=RunConfig(tracing_disabled=True),
    )
    print(result.final_output)


asyncio.run(main())
