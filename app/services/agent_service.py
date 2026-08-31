import logging

from app.core.exceptions import AgentMaxIterationsError, ToolError
from app.tools.registry import ToolRegistry
from app.llm.provider import LLMProvider

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

    

    def run(
        self,
        message: str,
    ) -> str:

        input_items = [
            {
                "role": "user",
                "content": message,
            }
        ]

        tools = self.tool_registry.get_definitions()
        

        for iteration in range(
            self.max_iterations
        ):

            logger.info(
                "Agent iteration=%s",
                iteration + 1,
            )
            
            response = (
                self.llm_provider.create_response(
                    input_items=input_items,
                    tools=tools,
                )
            )

            tool_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            if not tool_calls:
                return response.output_text


            input_items.extend(response.output)

            for tool_call in tool_calls:

                logger.info(
                    "Agent requested tool=%s",
                    tool_call.name,
                )
                try:
                    result = (
                        self.tool_registry.execute(
                            name=tool_call.name,
                            arguments=tool_call.arguments,
                        )
                    )

                    tool_output = str(result)

                    logger.info(
                            "Tool completed: tool=%s",
                            tool_call.name,
                    )
                except ToolError:
                    logger.warning(
                        "Tool failed: tool=%s",
                        tool_call.name,
                    )

                    tool_output = (
                        "The requested tool could not "
                        "complete the operation."
                    )

                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": tool_output,
                    }
                )


        raise AgentMaxIterationsError(
            self.max_iterations
        )