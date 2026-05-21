# 📚 Learnings

## Event Consumer

payment_worker.py became asynchronous consumer.

---

## Retry Handling

Transient failures should retry automatically.

---

## Poison Events

Some events fail permanently and must move to failed state.

This is foundation of DLQ architecture.

---

## Eventual Consistency

Ride completion and payment completion happen at different times.

Distributed systems synchronize state over time.

---

## Database Consolidation

Single source of truth reduces operational confusion.

---

## Authentication vs Authorization

Database login success does not guarantee table permissions.
