class AppError(Exception):
    pass


class TaskNotFoundError(AppError):

    def __init__(self, task_id: int):
        self.task_id = task_id

        super().__init__(
            f"Task {task_id} does not exist"
        )

class AgentError(AppError):
    pass

class LLMUnavailableError(AppError):
    pass


class ToolCallError(AppError):
    pass

class LLMProviderError(AppError):
    pass


class LLMRateLimitError(LLMProviderError):
    pass


class LLMAuthenticationError(LLMProviderError):
    pass

class AgentMaxIterationsError(
    AgentError
):
    def __init__(
        self,
        max_iterations: int,
    ):
        self.max_iterations = (
            max_iterations
        )

        super().__init__(
            "Agent exceeded maximum "
            f"iterations: {max_iterations}"
        )

class ToolError(AppError):
    pass


class UnknownToolError(ToolError):

    def __init__(
        self,
        tool_name: str,
    ):
        self.tool_name = tool_name

        super().__init__(
            f"Unknown tool: {tool_name}"
        )