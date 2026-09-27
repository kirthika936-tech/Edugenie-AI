from typing import List

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def clean_text(
    value: str,
    max_chars: int,
) -> str:

    value = value.strip()

    if not value:
        raise ValueError(
            "Input cannot be empty."
        )

    if len(value) > max_chars:
        raise ValueError(
            f"Input is too long. "
            f"Maximum is {max_chars} characters."
        )

    return value


# ---------------------------------------------------------
# Q&A
# ---------------------------------------------------------

class QARequest(BaseModel):

    question: str = Field(
        min_length=1
    )

    @field_validator("question")
    @classmethod
    def validate_question(
        cls,
        value: str,
    ) -> str:

        return clean_text(
            value,
            20000,
        )


# ---------------------------------------------------------
# Explanation
# ---------------------------------------------------------

class ExplainRequest(BaseModel):

    topic: str = Field(
        min_length=1
    )

    @field_validator("topic")
    @classmethod
    def validate_topic(
        cls,
        value: str,
    ) -> str:

        return clean_text(
            value,
            20000,
        )


# ---------------------------------------------------------
# Quiz
# ---------------------------------------------------------

class QuizRequest(BaseModel):

    text: str = Field(
        min_length=1
    )

    @field_validator("text")
    @classmethod
    def validate_text(
        cls,
        value: str,
    ) -> str:

        return clean_text(
            value,
            12000,
        )


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

class SummaryRequest(BaseModel):

    text: str = Field(
        min_length=1
    )

    @field_validator("text")
    @classmethod
    def validate_text(
        cls,
        value: str,
    ) -> str:

        return clean_text(
            value,
            20000,
        )


# ---------------------------------------------------------
# Learning path
# ---------------------------------------------------------

class LearningPathRequest(BaseModel):

    topic: str = Field(
        min_length=1
    )

    level: str = "beginner"

    @field_validator("topic")
    @classmethod
    def validate_topic(
        cls,
        value: str,
    ) -> str:

        return clean_text(
            value,
            500,
        )

    @field_validator("level")
    @classmethod
    def validate_level(
        cls,
        value: str,
    ) -> str:

        allowed = {
            "beginner",
            "intermediate",
            "advanced",
        }

        value = value.strip().lower()

        if value not in allowed:

            raise ValueError(
                "Level must be one of: "
                "beginner, intermediate, advanced."
            )

        return value


# ---------------------------------------------------------
# Generic text response
# ---------------------------------------------------------

class TextResponse(BaseModel):

    result: str


# ---------------------------------------------------------
# Quiz models
# ---------------------------------------------------------

class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4,
    )

    correct_answer: str

    explanation: str


class QuizResponse(BaseModel):

    questions: List[QuizQuestion] = Field(
        min_length=1,
        max_length=10,
    )


# ---------------------------------------------------------
# Learning path models
# ---------------------------------------------------------

class LearningStep(BaseModel):

    stage: str

    topics: List[str]

    estimated_time: str

    resources: List[str]


class LearningPathResponse(BaseModel):

    topic: str

    level: str

    steps: List[LearningStep]

    study_tips: List[str]