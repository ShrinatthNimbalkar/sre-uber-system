# Day 11 Failure Log

Use this incident pattern when revisiting the failures:

```text
Symptom -> Evidence -> Root cause -> Fix -> Verification
```

## Incident 1 - Flask module missing

**Symptom**

```text
ModuleNotFoundError: No module named 'flask'
```

**Root cause:** Flask was not installed in the active Python environment.

**Fix:** Installed Flask into the active virtual environment.

**Learning:** The application failed before any network or database interaction occurred. Follow the first failing layer instead of debugging downstream systems.

---

## Incident 2 - PostgreSQL Python driver missing

**Symptom**

```text
ModuleNotFoundError: No module named 'psycopg2'
```

A source install of `psycopg2` then failed with:

```text
pg_config executable not found
```

**Root cause:** The package attempted a native source build without PostgreSQL development tooling.

**Fix**

```bash
python -m pip install psycopg2-binary==2.9.11
```

**Verification**

```text
psycopg2 loaded: 2.9.11
```

---

## Incident 3 - PostgreSQL connection refused

**Symptom:** `POST /ride` returned HTTP 500.

```text
connection to server at "localhost", port 5432 failed: Connection refused
```

**Evidence**

```bash
lsof -nP -iTCP:5432 -sTCP:LISTEN
```

returned no listener, and Docker contained no PostgreSQL container.

**Root cause:** PostgreSQL had previously run inside an Ubuntu 22 VM that had been deleted.

**Fix:** Added PostgreSQL 16 to Docker Compose.

**Verification**

```text
/var/run/postgresql:5432 - accepting connections
```

---

## Incident 4 - Undefined Docker volume

**Symptom**

```text
service "postgres" refers to undefined volume postgres_data
```

**Root cause:** The service referenced the volume but the top-level named volume was not declared.

**Fix**

```yaml
volumes:
  postgres_data:
```

**Verification:** `docker compose ... config` rendered successfully.

---

## Incident 5 - Fresh database had no tables

**Symptom**

```text
Did not find any relations.
```

**Root cause:** The new PostgreSQL volume was healthy but empty.

**Fix:** Added and applied `services/ride-service/schema.sql`.

**Verification:** `\dt` showed `rides` and `events`, and `POST /ride` created `ride_id=1`.

## Failure pattern learned

```text
Python dependency
      -> native package/build dependency
      -> TCP service availability
      -> container/storage configuration
      -> database schema
```

Locate the failing layer first. Then fix that layer.
