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

System Interaction FlowGateway receives an execution request (via API or manual start) and reads the current orchestration Blueprint from GCS.The orchestrator spawns processing steps like a Vertex AI Batch Job or target LLM worker.Once completed, a native GCS Bucket Event fires.The event securely routes token data back into the stateless Router to evaluate the next step.Progress metrics and run details are stored back in the GCS Ledger.📋 What Lives inside the GCS Ledger?Rather than maintaining a heavy relational schema, everything required to run and trace a pipeline is contained inside flat, transaction-safe JSON files:🏗️ Pipeline Blueprints: Sequence of execution steps, including LLM calls and Multimedia Processing parameters (e.g., Image Resizing, Video Compression metadata).🧠 Model Metadata: Assigns LLM versions (e.g., swapping Gemini 3.1 Pro to Gemini 3.1 Flash-Lite) and details multi-model fallback routines.📜 System Instructions: Specific context-driven prompts, persona parameters, and tone constraints.📐 Response Schemas: Strictly structured Pydantic JSON targets to guarantee model outputs conform exactly to downstream database requirements.🧹 Lifecycle Rules: Explicit instructions telling the orchestrator when to move, archive, or delete temporary data payloads after execution completes.🚀 Scaling & Future-Proofing MatrixFeature / BenefitTechnical Realization🚦 Dual-Trigger ArchitectureTrigger execution flows simultaneously via standard POST payload requests or automatically when assets land in a GCS storage bucket.⚡ Zero RedeploymentsUpgrade models, fine-tune prompts, or modify DAG pathways instantly by editing a JSON blueprint. Skip the 5-minute CI/CD and container build bottlenecks.📊 Deterministic OutputForce AI outputs to conform to custom, hot-swapped schema definitions on the fly without breaking backend parser models.🛠️ Custom Processing StepsPlug pre-processing transformations (like scaling images) and post-processing tasks (like compressing outputs) directly into the JSON configuration file.🛡️ Future-Proof FoundationSeamlessly swap out decaying components or old prompts to match newly released LLMs (like Gemini 3.1) in seconds.📈 Infinite ScalingZero persistent database lock-ins. Compute layers scale instantly from 1 to 1,000,000 requests simultaneously.
