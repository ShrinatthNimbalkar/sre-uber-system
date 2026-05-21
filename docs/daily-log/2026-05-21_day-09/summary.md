# 📅 Day 09 — Event Consumption + Retry Architecture

## 🚀 What Was Built

- Introduced payment_worker.py
- Added asynchronous event consumption
- Added retry_count handling
- Added failed event state
- Simulated flaky downstream payment processing
- Consolidated architecture toward single DB source

---

## 🧠 Major Learning

Distributed systems assume failure is normal.

Consumers must:
- retry transient failures
- isolate poison events
- prevent infinite retry storms

---

## 🔥 Architecture Evolution

Producer:
Ride Service

Consumer:
payment_worker.py

Shared State:
events table

---

## 💡 Key Insight

Asynchronous systems require explicit failure-handling strategy.
