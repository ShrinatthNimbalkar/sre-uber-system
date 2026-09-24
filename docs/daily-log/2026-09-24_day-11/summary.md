# Day 11 Summary - Real Ride Completion Publishes to Kafka

## Objective

Connect the existing Ride Service to Kafka so that a real business action - completing a ride - automatically emits a payment event.

The goal was not merely to make a producer script work. The goal was to prove this real application path:

```text
HTTP request
   -> Ride Service
   -> PostgreSQL state change
   -> Kafka event publication
```

## Starting point

Before Day 11, the project had two mostly separate paths:

```text
Application path
Ride Service -> PostgreSQL events table -> Payment Worker

Kafka learning path
Demo Producer -> payment-events -> Demo Consumer
```

The Kafka producer generated a hard-coded `ride_id=101` every five seconds, so Kafka was not yet connected to real application behavior.

## What we built

### Reproducible PostgreSQL runtime

PostgreSQL had previously lived natively inside an Ubuntu 22 VM. That VM was later deleted, so the Ride Service failed with:

```text
connection to server at "localhost", port 5432 failed: Connection refused
```

PostgreSQL 16 was added to the existing Docker Compose stack.

### Persistent PostgreSQL storage

A named volume was added:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Docker Compose created the runtime volume `kafka-local_postgres_data`.

This separates the PostgreSQL container lifetime from the database-file lifetime.

### Schema as code

Created `services/ride-service/schema.sql` defining the `rides` and `events` tables and their foreign-key relationship.

### Reusable Kafka producer

The demo producer loop was replaced with a reusable application function:

```text
publish_payment_requested(ride_id)
```

The producer waits for broker acknowledgement and records the returned partition and offset.

### Ride Service integration

When a ride transitions to `completed`, the service now creates the existing PostgreSQL payment event and publishes the same business event to Kafka.

## End-to-end verification

Created ride:

```json
{"ride_id":1,"status":"requested"}
```

Lifecycle:

```text
requested -> assigned -> in_progress -> completed
```

Flask output after completion:

```text
Kafka accepted: ride_id=1, partition=0, offset=11
```

Kafka was independently inspected and returned:

```text
Offset:11  {"ride_id": 1, "event": "payment_requested"}
```

PostgreSQL showed the ride as `completed` and the `payment_requested` event as `pending` with retry count `0`.

## Architecture at the end of Day 11

```text
Client
  |
  v
Ride Service
  |
  +------> PostgreSQL
  |          |
  |          +-- rides
  |          `-- events
  |
  `------> Kafka Producer
               |
               v
          payment-events
```

## Why this matters

Kafka is no longer an isolated demonstration. A real application state transition now creates a real event in Kafka.

This also exposes the next production problem: PostgreSQL and Kafka are separate systems, so the two writes can succeed or fail independently.
