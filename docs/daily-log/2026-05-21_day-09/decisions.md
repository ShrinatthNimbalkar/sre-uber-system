# 🧠 Decisions

## 1. Introduce payment_worker.py

Reason:
Separate asynchronous payment processing from API path.

---

## 2. Add retry_count

Reason:
Support transient downstream failures.

---

## 3. Add failed event state

Reason:
Prevent infinite retry storms.

---

## 4. Consolidate toward sre_db

Reason:
Maintain single consistent database source.

---

## 5. Keep architecture simple

Reason:
Focus on event-driven concepts before multi-DB complexity.
