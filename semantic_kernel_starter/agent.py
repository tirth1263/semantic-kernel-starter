"""Factory helpers for the Semantic Kernel ChatCompletionAgent."""

from __future__ import annotations

from openai import AsyncOpenAI
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.functions import KernelArguments

from .config import AppSettings
from .plugins import TimePlugin


AGENT_NAME = "SemanticKernelStarterAgent"


def build_agent(settings: AppSettings) -> ChatCompletionAgent:
    """Create a ChatCompletionAgent backed by Nebius Token Factory."""

    kernel = Kernel()

    client = AsyncOpenAI(
        api_key=settings.nebius_api_key,
        base_url=settings.nebius_base_url,
    )

    service = OpenAIChatCompletion(
        ai_model_id=settings.nebius_model,
        async_client=client,
        service_id=settings.service_id,
    )
    kernel.add_service(service)
    kernel.add_plugin(
        TimePlugin(default_timezone=settings.default_timezone),
        plugin_name="time",
    )

    execution_settings = OpenAIChatPromptExecutionSettings(
        service_id=settings.service_id,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )

    return ChatCompletionAgent(
        kernel=kernel,
        name=AGENT_NAME,
        instructions=(
            "You are a concise, friendly AI assistant. Use available tools when "
            "they can answer the user more accurately, especially the time.now "
            "function for current date or time questions."
        ),
        arguments=KernelArguments(settings=execution_settings),
        function_choice_behavior=FunctionChoiceBehavior.Auto(),
    )


def create_thread() -> ChatHistoryAgentThread:
    """Create an agent thread that preserves conversation context."""

    return ChatHistoryAgentThread()

