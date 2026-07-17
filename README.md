# double-loop-orchestrator
A low-code, stateless, zero-database GCS-ledger architecture for hot-swapping LLMs, prompts, and schemas without re-deployment.

## 💡 The Core Philosophy: Configuration as Data

In traditional software, changing logic requires a code deployment. In the **Double-Loop** architecture, we **decouple the 'Brain' (Logic) from the 'Body' (Execution)**. By storing your system's intelligence in **Google Cloud Storage (GCS)** as JSON 'Blueprints', you transform infrastructure into a dynamic, live-updating organism.

┌──────────────────────────────┐
                  │      GCS: "The Brain"        │
                  │  - Pipe Blueprints (JSON)    │
                  │  - Job Ledgers (JSON)        │
                  └──────────────────────────────┘
                       ▲                  ▲
         1. Reads      │                  │ 4. Writes
            Config     │                  │    Progress
                       ▼                  │
   ┌───────────────────────┐    2. Spawns  ┌───────────────────────┐
   │    Gateway (Run)      │ ────────────> │  Vertex AI Batch Job  │
   └───────────────────────┘               └───────────────────────┘
               ▲                                       │
               │ 5. Trigger next stage                 │ 3. Notifies
               │                                       ▼
   ┌───────────────────────┐               ┌───────────────────────┐
   │    Router (Run)       │ <──────────── │  GCS Bucket Event     │
   └───────────────────────┘  Secure Token └───────────────────────┘
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
