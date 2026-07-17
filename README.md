Double-Loop Orchestrator 🚀

A low-code, stateless, zero-database GCS-ledger architecture for hot-swapping LLMs, prompts, and schemas without re-deployment.

💡 The Core Philosophy: Configuration as Data

In traditional software systems, modifying application logic requires a full code deployment cycle. The Double-Loop architecture solves this by strictly decoupling the "Brain" (System Logic) from the "Body" (Execution Compute).

By storing your system's intelligence and DAG instructions directly in Google Cloud Storage (GCS) as lightweight JSON "Blueprints", you transform static cloud infrastructure into a dynamic, live-updating organism.

System Interaction Flow

flowchart TB
    %% Nodes
    GCS["📂 Google Cloud Storage (The Brain)<br>• Pipe Blueprints (JSON)<br>• Job Ledgers (JSON)"]
    Gateway["⚡ Gateway (Cloud Run)"]
    Vertex["🧠 Vertex AI Batch Job"]
    Event["🔔 GCS Bucket Event"]
    Router["🔀 Router (Cloud Run)"]

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


🚦 Core Architecture & Dual-Trigger Loop

Your stateless orchestrator can be triggered either asynchronously via file uploads or synchronously via standard HTTP API calls. It reads configurations dynamically from the GCS "Brain" without needing database polling or persistent memory caches.

graph TD
    classDef brain fill:#e8f0fe,stroke:#4285f4,stroke-width:2px,color:#1a73e8,font-weight:bold;
    classDef gate fill:#fef7e0,stroke:#fbbc05,stroke-width:1px,color:#b06000,font-weight:bold;
    
    subgraph Trigger_Layer ["Traffic Control"]
        direction LR
        A["File Upload (GCS Event)"] -->|Invokes| C["Router (Cloud Function/Run)"]
        D["POST Payload (Direct API)"] -->|Invokes| E["Gateway (Cloud Function/Run)"]
    end

    subgraph Core_Loop ["The Orchestration Loop"]
        E -->|1. Reads Config| F["GCS 'The Brain' (Ledger)"]
        C -->|1. Reads Config| F
        E -->|2. Spawns| G["Vertex AI Batch Job"]
        G -->|3. Notifies| H["GCS Bucket Event"]
        H -->|4. Secure Token| C
        C -->|5. Writes Progress| F
    end

    class F brain;
    class E,C gate;


📋 What Lives inside the GCS Ledger?

Rather than maintaining a heavy relational schema, everything required to run and audibly trace a pipeline is contained inside flat, transaction-safe JSON files:

🏗️ Pipeline Blueprints: Sequence of execution steps, including LLM calls and Multimedia Processing parameters (e.g., Image Resizing, Video Compression metadata).

🧠 Model Metadata: Assigns LLM versions (e.g., swapping Gemini 3.1 Pro to Gemini 3.1 Flash-Lite) and details multi-model fallback routines.

📜 System Instructions: Specific context-driven prompts, persona parameters, and tone constraints.

📐 Response Schemas: Strictly structured Pydantic JSON targets to guarantee model outputs conform exactly to downstream database requirements.

🧹 Lifecycle Rules: Explicit instructions telling the orchestrator when to move, archive, or delete temporary data payloads after execution completes.

🚀 Scaling & Future-Proofing Matrix

Feature / Benefit

Technical Realization

🚦 Dual-Trigger Architecture

Trigger execution flows simultaneously via standard POST payload requests or automatically when assets land in a GCS storage bucket.

⚡ Zero Redeployments

Upgrade models, fine-tune prompts, or modify DAG pathways instantly by editing a JSON blueprint. Skip the 5-minute CI/CD and container build bottlenecks.

📊 Deterministic Output

Force AI outputs to conform to custom, hot-swapped schema definitions on the fly without breaking backend parser models.

🛠️ Custom Processing Steps

Plug pre-processing transformations (like scaling images) and post-processing tasks (like compressing outputs) directly into the JSON configuration file.

🛡️ Future-Proof Foundation

Seamlessly swap out decaying components or old prompts to match newly released LLMs (like Gemini 3.1) in seconds.

📈 Infinite Scaling

Zero persistent database lock-ins. Compute layers scale instantly from 1 to 1,000,000 requests without connection pool bottlenecks.

⚡ Getting Started

Interested in running the Double-Loop architecture yourself? Click the button below to launch an interactive sandbox in Google Colab. The demo contains a fully functional simulation mode (no GCP access needed) as well as an active GCS deployment guide.
