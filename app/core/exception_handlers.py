from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import LLMProviderError, LLMRateLimitError


async def task_not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    return JSONResponse(
        status_code=404,
        content={
            "error": "TASK_NOT_FOUND",
            "message": str(exc),
        },
    )


async def llm_unavailable_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    return JSONResponse(
        status_code=502,
        content={
            "error": "LLM_UNAVAILABLE",
            "message": str(exc),
        },
    )


async def tool_call_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    return JSONResponse(
        status_code=400,
        content={
            "error": "TOOL_CALL_ERROR",
            "message": str(exc),
        },
    )

async def llm_rate_limit_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    return JSONResponse(
        status_code=503,
        content={
            "error": "LLM_RATE_LIMIT",
            "message": (
                "The AI service is temporarily busy. "
                "Please try again later."
            ),
        },
    )

async def llm_provider_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:

    return JSONResponse(
        status_code=502,
        content={
            "error": "LLM_PROVIDER_ERROR",
            "message": (
                "The AI provider could not "
                "complete the request."
            ),
        },
    )

async def llm_authentification_error_handler(
    request: Request,
    exc: Exception,               # LLMProviderError,
) -> JSONResponse:

    return JSONResponse(
        status_code=500,
        content={
            "error": "LLM_AUTH_ERROR",
            "message": (
                "The AI provider could not "
                "complete the request."
            ),
        },
    )