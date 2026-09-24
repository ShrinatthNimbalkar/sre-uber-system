# Day 11 Learnings

## Database software is not the storage itself

PostgreSQL is a running database process that manages database files.

```text
Application
   -> PostgreSQL process
   -> database files
   -> filesystem
   -> persistent storage
```

A process can die while its data survives, provided the underlying storage has an independent lifetime.

## Container lifetime and data lifetime must be separated

```text
PostgreSQL container
        |
        v
/var/lib/postgresql/data
        |
        v
postgres_data Docker volume
```

The named volume protects against normal container replacement. It is not a backup and does not protect against destruction of the underlying Colima storage or host disk.

## Running is not the same as ready

Docker reported the PostgreSQL container as `Up`, but readiness was verified with `pg_isready`.

```text
process exists != application is ready to serve requests
```

## Git state and runtime state are different

Git stores reproducible definitions such as source code, Docker Compose, schema files, and configuration.

Runtime systems store live state such as PostgreSQL rows, Kafka records, and Docker volume contents.

## Schema as code makes structure reproducible

`schema.sql` defines the database shape required by the application. The schema is versioned; the actual rows are runtime state.

## Kafka offsets became concrete

The manual producer test wrote:

```text
offset 10 -> ride_id 999
```

The real Ride Service then produced:

```text
offset 11 -> ride_id 1
```

This demonstrated the append-only log behavior of partition 0.

## Broker acknowledgement is stronger evidence than a print statement

The producer waits for Kafka metadata containing the partition and offset. The event was then independently consumed from that location.

```text
application attempted publish
        -> broker acknowledged
        -> record independently consumed
```

## One business action now changes two systems

```text
Ride Service
   |
   +---> PostgreSQL write
   |
   `---> Kafka write
```

The next question is what happens when only one write succeeds. That is the bridge into distributed-systems consistency.
