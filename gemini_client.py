from typing import Type, TypeVar

from pydantic import BaseModel

from config import settings


T = TypeVar(
    "T",
    bound=BaseModel,
)


class GeminiNotConfiguredError(
    RuntimeError
):
    pass


# ---------------------------------------------------------
# Lazy SDK loading
# ---------------------------------------------------------

def _load_sdk():

    try:

        from google import genai

        from google.genai import types

        return genai, types

    except ImportError as exc:

        raise RuntimeError(
            "Google GenAI SDK is not installed. "
            "Run: pip install -r requirements.txt"
        ) from exc


# ---------------------------------------------------------
# Gemini client
# ---------------------------------------------------------

def get_client():

    if not settings.gemini_api_key:

        raise GeminiNotConfiguredError(
            "GEMINI_API_KEY is not configured. "
            "Copy .env.example to .env and add your API key."
        )

    genai, _ = _load_sdk()

    return genai.Client(
        api_key=settings.gemini_api_key
    )


# ---------------------------------------------------------
# Normal text generation
# ---------------------------------------------------------

def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
) -> str:

    _, types = _load_sdk()

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )

    text = (
        response.text or ""
    ).strip()

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text


# ---------------------------------------------------------
# Structured JSON generation
# ---------------------------------------------------------

def generate_structured(
    prompt: str,
    schema: Type[T],
    *,
    system_instruction: str | None = None,
    temperature: float = 0.2,
    max_output_tokens: int = 1600,
) -> T:

    _, types = _load_sdk()

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=schema,
    )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=config,
    )

    text = (
        response.text or ""
    ).strip()

    if not text:

        raise RuntimeError(
            "Gemini returned an empty structured response."
        )

    return schema.model_validate_json(
        text
    )