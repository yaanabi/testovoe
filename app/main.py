from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Response

from app.mocks import participants, registrations, workouts
from app.schemas import (
    Participant, ParticipantCreate, Registration, RegistrationCreate,
    Workout, WorkoutCreate, WorkoutUpdate,
)

app = FastAPI(
    title="Спортивные тренировки",
    description="моки.",
)


@app.get("/participants", response_model=list[Participant], tags=["Участники"])
def list_participants():
    return participants


@app.post("/participants", response_model=Participant, status_code=201, tags=["Участники"])
def create_participant(payload: ParticipantCreate):
    return {"id": 3, **payload.model_dump(), "created_at": datetime.now(timezone.utc)}


@app.get("/participants/{id}", response_model=Participant, tags=["Участники"])
def get_participant(id: int):
    for participant in participants:
        if participant["id"] == id:
            return participant
    raise HTTPException(status_code=404, detail="Участник не найден")


@app.get("/workouts", response_model=list[Workout], tags=["Тренировки"])
def list_workouts():
    return workouts


@app.post("/workouts", response_model=Workout, status_code=201, tags=["Тренировки"])
def create_workout(payload: WorkoutCreate):
    return {"id": 3, **payload.model_dump()}


@app.get("/workouts/{id}", response_model=Workout, tags=["Тренировки"])
def get_workout(id: int):
    for workout in workouts:
        if workout["id"] == id:
            return workout
    raise HTTPException(status_code=404, detail="Тренировка не найдена")


@app.patch("/workouts/{id}", response_model=Workout, tags=["Тренировки"])
def update_workout(id: int, payload: WorkoutUpdate):
    workout = get_workout(id)
    return {**workout, **payload.model_dump(exclude_unset=True)}


@app.get("/registrations", response_model=list[Registration], tags=["Записи"])
def list_registrations(participant_id: int | None = None, workout_id: int | None = None):
    return [
        registration for registration in registrations
        if (participant_id is None or registration["participant_id"] == participant_id)
        and (workout_id is None or registration["workout_id"] == workout_id)
    ]


@app.post("/registrations", response_model=Registration, status_code=201, tags=["Записи"])
def create_registration(payload: RegistrationCreate):
    return {"id": 2, **payload.model_dump(), "created_at": datetime.now(timezone.utc)}


@app.delete("/registrations/{id}", status_code=204, tags=["Записи"])
def delete_registration(id: int):
    for registration in registrations:
        if registration["id"] == id:
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Запись не найдена")
