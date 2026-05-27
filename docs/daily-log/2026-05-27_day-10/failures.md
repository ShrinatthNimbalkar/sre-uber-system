# 💥 Failures

## 1. Docker Compose Version Confusion

System used:
docker-compose

Instead of:
docker compose

Reason:
Ubuntu package installed older Compose v1 binary.

---

## 2. Kafka Conceptual Shift

Initial thinking:
Kafka behaves like queue.

Correct understanding:
Kafka behaves like distributed immutable event log.

---

## 🔥 Learning

Infrastructure tooling versions vary heavily across environments.

Always verify actual installed runtime behavior.
