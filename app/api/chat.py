from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.schemas.ai import EmailSummary, EmailRequest
from app.services.openai_service import OpenAILLMService
from app.llm.openai import OpenAIProvider

from fastapi import Depends


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


def get_llm_service() -> OpenAILLMService:

    provider = OpenAIProvider()
    return OpenAILLMService(provider)

@router.post(
    "/",
    response_model=ChatResponse,
)

def chat(request: ChatRequest,
         service: OpenAILLMService = Depends(get_llm_service)):

    answer = service.generate_with_tools(
        request.message
    )

    return ChatResponse(
        answer=answer
    )


@router.get(
    "/person",
)
def person(service: OpenAILLMService = Depends(get_llm_service)):

    person = service.extract_person(
        "Allice us a 32 years old"
    )

    return person

@router.post(
    "/summarize-email",
    response_model=EmailSummary,
)

def email_summerized(email:EmailRequest,
                     service: OpenAILLMService = Depends(get_llm_service)):

    answer = service.summarize_email(
        email.email
    )

    return answer