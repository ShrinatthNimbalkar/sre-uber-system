# 📅 Day 10 — Real Kafka Infrastructure + Streaming

## 🚀 What Was Built

- Installed Kafka locally using Docker Compose
- Installed Zookeeper
- Created Kafka broker
- Created payment-events topic
- Built Python Kafka producer
- Built Python Kafka consumer
- Streamed real events through Kafka
- Introduced partition and consumer group concepts

---

## 🧠 Major Learning

Kafka is not a traditional queue.

Kafka is a distributed append-only event log.

---

## 🔥 Architecture Evolution

Before:
Ride Service → PostgreSQL polling worker

After:
Producer → Kafka Broker → Consumer

---

## 💡 Key Insight

Databases store current state.

Kafka stores history of events over time.
