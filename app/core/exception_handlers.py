from fastapi import Request
from fastapi.responses import JSONResponse


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

