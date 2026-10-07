# Ente's Go server (museum)

Read this for any server question.

## What museum is

A single Go binary. One entrypoint at `server/cmd/museum/main.go` wires every
repository, controller and handler by hand — there is no dependency injection
framework — registers ~273 routes, starts cron jobs, and listens on 8080.

| Path | What lives there |
|---|---|
| `server/cmd/museum/main.go` | wiring, route table, cron schedule |
| `server/ente/` | plain structs: request bodies, DB rows, sentinel errors |
| `server/pkg/api/` | HTTP handlers — bind JSON, call a controller, write JSON |
| `server/pkg/controller/` | business rules: permissions, validation, orchestration |
| `server/pkg/repo/` | the SQL; the only layer that knows table names |
| `server/pkg/middleware/` | auth, rate limits, request logging, panic recovery |
| `server/pkg/utils/` | crypto, auth header helpers, JSON binding, error mapping |
| `server/migrations/` | numbered `.up.sql`/`.down.sql` pairs, applied at boot |
| `server/internal/testutil/` | throwaway test DB, table reset, user fixtures |
| `server/space/` | Ente Space, a separate product with the same layering |

The rule that makes it navigable: **rules live in the controller, SQL lives in the repo.**
"Why was I not allowed to do that?" → controller. "What actually changed?" → repo.

## Topics he may ask about

Auth and identity: the `tokens` table and why only a hash is stored; `X-Auth-Token` vs
`X-Auth-User-ID`; the middleware chain and the route groups in main.go (`publicAPI`,
`privateAPI`, `storageAPI`, `adminAPI`, link-token groups); JWT-scoped routes; how
tests fake auth.

Request lifecycle: Gin routing; middleware order; `handler.BindJSON` and `binding:"required"`;
`stacktrace.Propagate`; how errors become status codes in `pkg/utils/handler`; sentinel
errors in `ente/errors.go`; the request logger and `req_id`.

Data layer: transactions and `defer tx.Rollback()`; `SELECT ... FOR UPDATE` row locks;
upserts via `ON CONFLICT`; why nothing is hard-deleted; `updation_time` as the entire
sync mechanism; diff endpoints and cursors.

Background work: queue tables written inside the transaction; crons in main.go;
distributed locks; the trash lifecycle from tap to bytes leaving S3.

Crypto boundary: what the server can and cannot see; key attributes; sealed boxes;
collection keys; `key.encryption` vs `key.hash` and why one is deterministic; why
length-only validation is all the server can do.

Operations: viper config layering; migrations and dirty state; object storage and
presigned URLs; rate limiting; usage and storage accounting; the multi-app split
(photos / auth / locker) in one server and database.

Testing: `server/internal/testutil`; controller tests with a partially-filled struct;
running against a local Postgres; driving the real HTTP API without a client.

## Running things locally

The local stack is Postgres.app (or Homebrew postgres) plus `go run cmd/museum/main.go`
from `server/`, which applies migrations at boot. Helper scripts may exist under
`server/scripts/` — check before writing your own. `psql -P pager=off -d ente_db -c "..."`
inspects the database; without `-P pager=off` psql pipes output through `less` and looks
like it hung.

Before claiming a test or command passes, run it. If the environment is not up and
bringing it up is slow, say what you did not verify rather than implying you did.

## Critical concepts get 2–3 real examples, not one

Some mechanisms are load-bearing — half the codebase leans on them. For these, one
example reads as trivia; two or three sightings in different places reveal the pattern.
When you explain any of the following (or anything similarly central), show it in
**2–3 different real endpoints or files**, each cited and quoted, each with one line on
what is different about this occurrence — then close with a single sentence stating the
invariant all of them share:

- The middleware auth handoff (`X-Auth-Token` in, `X-Auth-User-ID` written) — e.g. how
  a share call, a file upload, and an account call all read identity the same way.
- `updation_time` as the entire sync mechanism — e.g. the bump in sharing, in
  add-files, and in trashing, and the diff queries that read it.
- Soft delete (`is_deleted = true`, never `DELETE`) — e.g. collection_files on move,
  collection_shares on unshare, tokens on logout.
- Transactions with `defer tx.Rollback()` and row locks — e.g. two or three repo
  functions that follow the identical open/lock/mutate/commit shape.
- `ON CONFLICT` upserts making writes retry-safe — e.g. re-adding a file, re-sharing
  an album, re-trashing a file.
- Queue tables written inside the transaction, drained later by crons — e.g. object
  deletion, compliance holds, empty-trash requests.
- Length-only validation at the crypto boundary — e.g. collection keys, sealed share
  keys, key attributes.

For narrow questions ("what does this one function do?") one well-chosen example is
fine — the multi-example rule is for concepts, not lookups.

## Running things locally

The local stack is Postgres.app (or Homebrew postgres) plus `go run cmd/museum/main.go`
from `server/`, which applies migrations at boot. Helper scripts may exist under
`server/scripts/` — check before writing your own. `psql -P pager=off -d ente_db -c "..."`
inspects the database; without `-P pager=off` psql pipes output through `less` and looks
like it hung.

Before claiming a test or command passes, run it. If the environment is not up and
bringing it up is slow, say what you did not verify rather than implying you did.
