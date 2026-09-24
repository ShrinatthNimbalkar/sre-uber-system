# Day 11 Architecture Decisions

## Run PostgreSQL in the local Docker Compose environment

**Context:** The Ride Service depended on PostgreSQL running in an Ubuntu VM that no longer existed.

**Decision:** Add PostgreSQL 16 to `kafka-local/docker-compose.yml`.

**Why:** Local infrastructure should be reproducible from the repository instead of depending on manually configured machines.

**Trade-off:** This is a learning environment, not a production high-availability PostgreSQL topology.

---

## Persist PostgreSQL with a named Docker volume

**Decision**

```text
postgres_data -> /var/lib/postgresql/data
```

**Why:** Database data should not have the same lifetime as the PostgreSQL container.

**Failure boundary:** This protects against normal container replacement, not deletion/corruption of the underlying host or Colima storage.

---

## Store the database schema in Git

**Decision:** Add `services/ride-service/schema.sql`.

**Why:** A fresh environment must be able to recreate the database structure.

```text
schema.sql      -> versioned structure
PostgreSQL rows -> runtime state
```

---

## Convert the Kafka producer into a reusable application component

**Before:** The producer continuously emitted a hard-coded `ride_id=101` event.

**Decision:** Expose `publish_payment_requested(ride_id)`.

**Why:** Real application behavior should cause events; the producer should only handle transport.

---

## Wait for Kafka acknowledgement

**Decision:** Wait for the producer future and inspect returned metadata.

**Why:** Broker acknowledgement with partition and offset is stronger evidence than logging "Sent" immediately after an asynchronous send.

Verified result:

```text
partition=0
offset=11
```

---

## Keep the PostgreSQL event write while also publishing to Kafka

**Current behavior**

```text
Ride Service
   |
   +---> create PostgreSQL payment_requested row
   |
   `---> publish payment_requested to Kafka
```

**Why keep it temporarily:** This deliberately exposes the next problem we want to study: two independent writes with different failure modes.

**Known risk**

```text
PostgreSQL commit succeeds
Kafka publish fails
```

The two systems can disagree about whether the payment event exists.

**Next:** Reproduce the failure before evaluating a more reliable pattern such as Transactional Outbox.
