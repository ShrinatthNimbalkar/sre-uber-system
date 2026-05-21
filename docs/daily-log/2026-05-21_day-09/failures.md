# 💥 Failures

## 1. Database Mismatch

Application pointed to:
ride_db

Events table existed in:
sre_db

Result:
relation "events" does not exist

---

## 2. Schema Migration Failure

Attempted direct pg_dump restore caused:
- duplicate table creation
- schema mismatch
- incompatible columns

Reason:
Old rides schema differed from new schema.

---

## 3. PostgreSQL Permission Failure

Worker failed with:
permission denied for table events

Reason:
sre_user lacked table grants.

Fix:
Granted table + sequence permissions.

---

## 🔥 Learning

Production failures often involve:
- config drift
- schema mismatch
- privilege misconfiguration
