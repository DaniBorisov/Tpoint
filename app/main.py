from fastapi import FastAPI

from app.api.tasks import router as task_router
from app.api.messages import router as messages_router
from app.api.chat import router as chat_router

from app.core.exceptions import TaskNotFoundError, LLMUnavailableError, ToolCallError, LLMRateLimitError, LLMProviderError, LLMAuthenticationError
from app.core.exception_handlers import (
    task_not_found_handler,
    llm_unavailable_handler,
    tool_call_error_handler,
    llm_provider_error_handler,
    llm_rate_limit_handler,
    llm_authentification_error_handler,
)

from app.core.logging_config import configure_logging

configure_logging()

app = FastAPI()

@app.get("/")
def root():
    return {"project": "AI assistant exercise",
            "version": "1.0",
            "author": "Daniel"}

app.include_router(task_router)
app.include_router(messages_router)
app.include_router(chat_router)

app.add_exception_handler(
    TaskNotFoundError,
    task_not_found_handler,
)
app.add_exception_handler(
    LLMUnavailableError,
    llm_unavailable_handler,
)
app.add_exception_handler(
    ToolCallError,
    tool_call_error_handler,
)
app.add_exception_handler(
    LLMRateLimitError,
    llm_rate_limit_handler,
)
app.add_exception_handler(
    LLMProviderError,
    llm_provider_error_handler,
)
app.add_exception_handler(
    LLMAuthenticationError,
    llm_authentification_error_handler,
)