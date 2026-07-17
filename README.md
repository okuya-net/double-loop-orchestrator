# Double-Loop Orchestrator 🚀

A low-code, stateless, zero-database GCS-ledger architecture for hot-swapping LLMs, prompts, and schemas without re-deployment.

## 💡 The Core Philosophy: Configuration as Data

In traditional software systems, modifying application logic requires a full code deployment cycle. The Double-Loop architecture solves this by strictly decoupling the "Brain" (System Logic) from the "Body" (Execution Compute).

By storing your system's intelligence and DAG instructions directly in Google Cloud Storage (GCS) as lightweight JSON "Blueprints", you transform static cloud infrastructure into a dynamic, live-updating organism.

```text
               ┌──────────────────────────────┐
               │      GCS: "The Brain"        │
               │  - Pipe Blueprints (JSON)    │
               │  - Job Ledgers (JSON)        │
               └──────────────────────────────┘
                    ▲                  ▲
      1. Reads      │                  │ 5. Writes
         Config     │                  │    Progress
                    ▼                  │
┌───────────────────────┐    2. Spawns  │
│    Gateway (Run)      │ ─────────────┼──────────────────────┐
└───────────────────────┘              │                      ▼
            ▲                          │          ┌───────────────────────┐
            │ 6. Trigger next stage    │          │  Vertex AI Batch Job  │
            │                          │          └───────────────────────┘
┌───────────────────────┐              │                      │
│    Router (Run)       │ <────────────┴──────────────────────┘
└───────────────────────┘            3. GCS Bucket Event / 4. Secure Token
