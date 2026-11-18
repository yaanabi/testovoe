from datetime import datetime
from typing import Annotated, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, EmailStr, Field, model_validator


Id = Annotated[int, Field(gt=0, le=2_147_483_647)]
Name = Annotated[str, Field(min_length=1, max_length=100)]


class Schema(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ParticipantCreate(Schema):
    name: Name
    email: Annotated[EmailStr, Field(max_length=255)]


class Participant(ParticipantCreate):
    id: Id
    created_at: datetime


class WorkoutCreate(Schema):
    title: Name
    trainer_name: Name
    starts_at: AwareDatetime
    duration_minutes: Id
    capacity: Id


class Workout(WorkoutCreate):
    id: Id


class WorkoutUpdate(Schema):
    title: Name | None = None
    trainer_name: Name | None = None
    starts_at: AwareDatetime | None = None
    duration_minutes: Id | None = None
    capacity: Id | None = None

    @model_validator(mode="after")
    def reject_explicit_null(self) -> Self:
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Поля тренировки не могут быть null")
        return self


class RegistrationCreate(Schema):
    participant_id: Id
    workout_id: Id


class Registration(RegistrationCreate):
    id: Id
    created_at: datetime
