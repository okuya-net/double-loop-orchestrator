# double-loop-orchestrator
A low-code, stateless, zero-database GCS-ledger architecture for hot-swapping LLMs, prompts, and schemas without re-deployment.

## 💡 The Core Philosophy: Configuration as Data

In traditional software, changing logic requires a code deployment. In the **Double-Loop** architecture, we **decouple the 'Brain' (Logic) from the 'Body' (Execution)**. By storing your system's intelligence in **Google Cloud Storage (GCS)** as JSON 'Blueprints', you transform infrastructure into a dynamic, live-updating organism.

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
---

## 🚦 Core Architecture & Dual-Trigger Loop

Your stateless orchestrator can be triggered either asynchronously via file uploads or synchronously via standard HTTP API calls. It reads configurations dynamicially from the GCS "Brain" without needing database polling.

```mermaid
graph TD
    classDef brain fill:#f9f,stroke:#333,stroke-width:2px;
    classDef gate fill:#bbf,stroke:#333,stroke-width:1px;
    
    subgraph Trigger_Layer ["Traffic Control"]
        direction LR
        A["File Upload (GCS Event)"] -->|Invokes| C["Router (Cloud Function)"]
        D["POST Payload (Direct API)"] -->|Invokes| E["Gateway (Cloud Function)"]
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

### **What lives in the Ledger?**

*   **🏗️ Pipeline Blueprints:** Sequence of steps including LLM calls and **Multimedia Processing** (e.g., Image Resizing, Video Compression).
*   **🧠 Model Metadata:** Assign LLM versions (e.g., Gemini 3.1 Pro vs. Flash-Lite) and support multi-model fallback logic.
*   **📜 System Instructions:** Specific prompts, persona definitions, and tone control.
*   **📐 Response Schemas:** Pydantic JSON structures to ensure the LLM responses will be written in the format you can immediately parse to your database.
*   **🧹 Lifecycle Rules:** Instructions for the orchestrator to **move, archive, or delete** processed files once finished.

---

## 🚀 Why this matters for Scaling & Future-Proofing

| Benefit | Description |
| :--- | :--- |
| ** **🚦 Dual-Trigger Architecture: GCS Event & Direct HTTP API** |Trigger by sending a standard POST payload to run the identical orchestrator logic, or by direct uploads to GCS bucket/drive, and GCS triggers the orchestrator immediately.
| **⚡ Zero Redeployments** | Upgrade models or change prompts by editing a JSON file. No CI/CD pipelines, no downtime. |
| **📊 Deterministic Output** | Update **Response Schemas** on the fly to support new UI features without refactoring the orchestrator. |
| **🛠️ Custom Processing** | Easily insert pre-processing (Image Resize) or post-processing (Compression) steps without refactoring core logic. |
| **🛡️ Future-Proofing** | The LLM landscape evolves weekly. Don't let your code rot; 'hot-swap' to newer models like Gemini 3.1 in seconds. |
| **📈 Infinite Scaling** | Stateless execution means you can process 1 file or 1 million simultaneously with no database bottlenecks. |

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/okuya-net/double-loop-orchestrator/blob/main/Double_Loop.ipynb)
