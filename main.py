"""Command-line entry point for the Semantic Kernel starter."""

from __future__ import annotations

import asyncio
import sys

from semantic_kernel_starter.agent import build_agent, create_thread
from semantic_kernel_starter.config import AppSettings


EXIT_COMMANDS = {"/exit", "/quit", "exit", "quit", "q"}


async def stream_agent_response(agent, thread, user_message: str):
    """Stream a single assistant response to stdout."""

    print("Assistant > ", end="", flush=True)

    async for response in agent.invoke_stream(messages=user_message, thread=thread):
        thread = response.thread
        chunk = response.message.content or ""
        if chunk:
            print(chunk, end="", flush=True)

    print()
    return thread


async def run_chat() -> None:
    """Run either a one-shot prompt or an interactive chat loop."""

    settings = AppSettings.from_env()
    agent = build_agent(settings)
    thread = create_thread()

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:]).strip()
        if prompt:
            await stream_agent_response(agent, thread, prompt)
        return

    print("Semantic Kernel Starter")
    print(f"Model: {settings.nebius_model}")
    print(f"Endpoint: {settings.nebius_base_url}")
    print("Type a message, or /exit to quit.")
    print()

    while True:
        try:
            user_message = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if not user_message:
            continue
        if user_message.lower() in EXIT_COMMANDS:
            return

        thread = await stream_agent_response(agent, thread, user_message)


def main() -> None:
    try:
        asyncio.run(run_chat())
    except RuntimeError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

