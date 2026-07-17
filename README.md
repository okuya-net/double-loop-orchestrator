# double-loop-orchestrator
A low-code, stateless, zero-database GCS-ledger architecture for hot-swapping LLMs, prompts, and schemas without re-deployment.

## 💡 The Core Philosophy: Configuration as Data

In traditional software, changing logic requires a code deployment. In the **Double-Loop** architecture, we **decouple the 'Brain' (Logic) from the 'Body' (Execution)**. By storing your system's intelligence in **Google Cloud Storage (GCS)** as JSON 'Blueprints', you transform infrastructure into a dynamic, live-updating organism.

---

## 🚦 Dual-Trigger Architecture: GCS Event vs. Direct HTTP API

Your stateless orchestrator can be triggered in two ways depending on your system's integration needs:

```mermaid
graph TD
    subgraph Event-Driven (Async)
        A[File Uploaded] -->|Triggers| B(GCS Cloud Event)
        B -->|Invokes| C[Cloud Function Router]
    end
    subgraph Direct API (Sync)
        D[Frontend / Webhook Client] -->|POST Request| E(HTTPS Gateway)
        E -->|Invokes| C
    end
    C -->|1. Reads Blueprint| F[GCS Ledger Bucket]
    C -->|2. Orchestrates Logic| G[Gemini 3.1 LLMs]

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
