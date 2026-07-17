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

### System Interaction Flow

```mermaid
flowchart TB
    %% Nodes
    GCS["GCS: The Brain (Pipe Blueprints & Job Ledgers JSON)"]
    Gateway["Gateway (Cloud Run / Function)"]
    Vertex["Vertex AI Batch Job"]
    Event["GCS Bucket Event Trigger"]
    Router["Router (Cloud Run / Function)"]

    %% Flow Layout & Interactions
    Gateway <-->| "1. Reads/Writes State" | GCS
    Gateway -->| "2. Spawns" | Vertex
    Vertex -->| "4. Writes Progress" | GCS
    Vertex -.->| "3. Notifies" | Event
    Event -->| "Secure Token" | Router
    Router -->| "5. Trigger Next Stage" | Gateway

    %% Styling (GCP inspired color palette)
    classDef default fill:#fafafa,stroke:#333,stroke-width:1px,color:#333;
    style GCS fill:#e8f0fe,stroke:#4285f4,stroke-width:2px,color:#1a73e8,font-weight:bold
    style Gateway fill:#fef7e0,stroke:#fbbc05,stroke-width:2px,color:#b06000,font-weight:bold
    style Vertex fill:#e6f4ea,stroke:#34a853,stroke-width:2px,color:#137333,font-weight:bold
    style Event fill:#fce8e6,stroke:#ea4335,stroke-width:2px,color:#c5221f,font-weight:bold
    style Router fill:#f3e8fd,stroke:#a142f4,stroke-width:2px,color:#681da8,font-weight:bold
