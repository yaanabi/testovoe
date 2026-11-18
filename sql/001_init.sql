BEGIN;

CREATE TABLE participants (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL CHECK (length(btrim(name)) > 0),
    email VARCHAR(255) NOT NULL UNIQUE CHECK (length(btrim(email)) > 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE workouts (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(100) NOT NULL CHECK (length(btrim(title)) > 0),
    trainer_name VARCHAR(100) NOT NULL CHECK (length(btrim(trainer_name)) > 0),
    starts_at TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    capacity INTEGER NOT NULL CHECK (capacity > 0)
);

CREATE TABLE registrations (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    participant_id INTEGER NOT NULL REFERENCES participants(id) ON DELETE RESTRICT,
    workout_id INTEGER NOT NULL REFERENCES workouts(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (participant_id, workout_id)
);

CREATE INDEX registrations_workout_id_idx ON registrations(workout_id);

COMMIT;
