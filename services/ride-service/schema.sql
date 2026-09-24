CREATE TABLE rides (
    ride_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    pickup_location TEXT NOT NULL,
    drop_location TEXT NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    ride_id INTEGER NOT NULL REFERENCES rides(ride_id),
    event_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    retry_count INTEGER NOT NULL DEFAULT 0
);
