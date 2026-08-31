import logging

from app.core.exceptions import AgentMaxIterationsError, ToolError
from app.llm.base import LLMProvider
from app.schemas.ai import EmailSummary, PersonInfo
from app.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class AgentService:

    def __init__(
        self,
        llm_provider: LLMProvider,
        tool_registry: ToolRegistry,
        max_iterations: int = 5,
    ):
        self.llm_provider = llm_provider
        self.tool_registry = tool_registry
        self.max_iterations = max_iterations

    async def run(
        self,
        message: str,
    ) -> str:
        messages = self.llm_provider.build_messages(message)
        tools = self.tool_registry.get_definitions()

        for iteration in range(self.max_iterations):
            logger.info(
                "Agent iteration=%s",
                iteration + 1,
            )

            response = await self.llm_provider.chat_response(
                messages=messages,
                tools=tools,
            )

            tool_calls = [
                item
                for item in response.output
                if item["type"] == "function_call"
            ]

            if not tool_calls:
                return response.output_text

            self.llm_provider.append_assistant_output(
                messages,
                response,
            )

            for call in tool_calls:
                logger.info(
                    "Agent requested tool=%s",
                    call["name"],
                )
                try:
                    result = self.tool_registry.execute(
                        name=call["name"],
                        arguments=call["arguments"],
                    )
                    tool_output = str(result)
                    logger.info(
                        "Tool completed: tool=%s",
                        call["name"],
                    )
                except ToolError:
                    logger.warning(
                        "Tool failed: tool=%s",
                        call["name"],
                    )
                    tool_output = (
                        "The requested tool could not "
                        "complete the operation."
                    )

                self.llm_provider.append_tool_output(
                    messages,
                    call_id=call["call_id"],
                    result=tool_output,
                )

        raise AgentMaxIterationsError(
            self.max_iterations
        )

    async def extract_person(
        self,
        text: str,
    ) -> PersonInfo:
        return await self.llm_provider.extract_person(text) # type: ignore

    async def summarize_email(
        self,
        email: str,
    ) -> EmailSummary:
        return await self.llm_provider.summarize_email(email) # type: ignore
