# 📊 VoxInsight: The Self-Healing Voice of Customer (VoC) Pipeline

VoxInsight is an enterprise-tier data processing and telemetry engine designed to transform chaotic, unstructured customer interactions (Gong calls, Zendesk support tickets, Intercom chats) into clean, structured, and quantifiable feature development priorities. 

By leveraging ultra-low latency infrastructure via **Groq (Llama-3.3)** and combining it with deterministic Python validation layers, VoxInsight eliminates the core failure modes of LLMs—hallucinations and high API latency—to deliver product insights that engineering teams can instantly trust.

Live Application Link: **[YOUR_STREAMLIT_APP_URL_HERE]**

---

## 🏗️ System Architecture

The core engineering strategy decouples the data ingestion, AI processing, and validation rules to guarantee system uptime, cost management, and perfect data traceability.

+---------------------------------------------------------------------------------+
|                                INGESTION LAYER                                  |
|  [ Gong Call Logs (Long) ]   [ Intercom Chats (Mid) ]   [ Zendesk Tickets (Short) ] |
+---------------------------------------------------+-----------------------------+
|
v
+---------------------------------------------------------------------------------+
|                                ORCHESTRATION LAYER                              |
|           - Regex Whitespace & Conversational Artifact Filtering               |
|           - Input Token Buffer Budget Enforcement (Safety Guard)                |
+---------------------------------------------------+-----------------------------+
|
v
+---------------------------------------------------------------------------------+
|                                AI PROCESSING ENGINE                             |
|          - Groq Hardware Execution Network (Llama-3.3-70b Inference)             |
|          - Enforced Schema Validation Contracts (Strict JSON Mode)               |
+---------------------------------------------------+-----------------------------+
|
v
+---------------------------------------------------------------------------------+
|                         DETERMINISTIC GUARDRAILS (POST-AI)                      |
|       [ Substring Pattern Match Check ] ------> Verifies Quote Verbatim         |
|                                                   |                             |
|              +------------------------------------+----------------------+      |
|              | (Passes Traceability)                                     | (Fails)|
|              v                                                           v      |
|     [ Verified Safe Data ]                                      [ Hallucination Flag ]
+--------------+------------------------------------------------------------------+
|
v
+---------------------------------------------------------------------------------+
|                               PRESENTATION & TELEMETRY                          |
|         - Executive PM Priority Matrix Dashboard (Plotly & Analytics)           |
|         - Trace-To-Source Visual Validation Split-Screen (Playground)           |
+---------------------------------------------------------------------------------+


---

## 🌟 Core System Capabilities

### 1. Lightning-Fast Analysis (Powered by Groq)
By migrating from legacy models to the **Groq Llama-3.3-70b-versatile** engine, text extraction delays drop from several seconds down to **200–400 milliseconds**. This makes it viable for high-volume enterprise production processing.

### 2. Anti-Hallucination Data Guardrails
AI metrics are useless if the underlying data can't be trusted. VoxInsight solves this by running a deterministic string verification check on the extracted customer text. If the AI "paraphrases" or creates an quote, the platform flags the entry to keep the database accurate.

### 3. Dynamic Anomaly Alert Signals
The analytics engine features an automated **Trend Anomaly Watchdog**. It calculates shifting averages over a 90-day rolling timeline. If customer sentiment drops heavily within a specific feature module, an executive-level system alert is instantly generated.

---

## 🛠️ Technology Stack & Dependencies

* **Frontend Dashboard UI:** Streamlit (Multi-page configuration routing)
* **High-Speed Inference Network:** Groq SDK (`llama-3.3-70b-versatile`)
* **Strict Structural Protocols:** Python `Enum` & custom schema JSON mapping contracts
* **Data Presentation Engine:** Pandas & Plotly (Rolling sentiment trajectories)
* **Pipeline Defensiveness:** Tenacity (Exponential wait/retry backoff loop handlers)

---

## 📂 Repository Directory Layout

```text
voxinsight-pipeline/
│
├── .streamlit/
│   └── secrets.toml          # Production environment token storage (Excluded via .gitignore)
│
├── app/
│   ├── main.py               # Application router & layout configuration
│   ├── dashboard.py          # Tab 1: Executive Analytics Dashboard & Telemetry
│   ├── playground.py         # Tab 2: Live AI Playground & Split-Screen Trace Audit
│   └── strategy_page.py      # Tab 3: Technical Implementation Strategy Brief
│
├── core/
│   ├── __init__.py
│   ├── pipeline.py           # Core Groq processing engine & extraction configuration
│   └── guards.py             # Deterministic verification & anti-hallucination guardrails
│
├── data/
│   └── mock_historical.csv   # Synthesized 90-day telemetry dataset (Includes built-in anomalies)
│
├── scripts/
│   └── generate_mock_data.py # Automated historical data synthesis generation script
│
├── .gitignore                # System-level version control exception file
└── requirements.txt          # Explicitly pinned production dependencies
🚀 Local Deployment Setup
Follow these commands to clone, initialize, and execute the system environment locally:

Bash
# 1. Clone your project repository
git clone [https://github.com/YOUR_GITHUB_USERNAME/voxinsight-pipeline.git](https://github.com/YOUR_GITHUB_USERNAME/voxinsight-pipeline.git)
cd voxinsight-pipeline

# 2. Build local virtual environment isolation layers using uv
uv venv
.venv\Scripts\Activate.ps1  # For Windows users
source .venv/bin/activate   # For Mac/Linux users

# 3. Install fully pinned production package dependencies
uv pip install -r requirements.txt

# 4. Generate the 90-day anomaly database file
python scripts/generate_mock_data.py

# 5. Fire up the local web engine server
uv run streamlit run app/main.py
📑 Strategic Business Context
VoxInsight was engineered to map directly to standard software delivery workflows:

Short-Form Content (Intercom Chat): Low processing cost, high immediacy. Instantly tracks immediate operational roadblocks and breaking UI bugs.

Medium-Form Content (Zendesk Support): High structural density. Optimizes resources by routing directly into categorized support metrics.

Long-Form Content (Gong Call Logs): High conversation noise. Strips out introductory chatter and scheduling text to keep processing costs low and prevent context errors.


***

## 🔄 How to Push and Update GitHub Neatly

Whenever you make changes to your local files and want to update your public GitHub repository cleanly, use this sequential step-by-step terminal routine:

```bash
# 1. Check which files have been modified or added
git status

# 2. Stage all modifications (your .gitignore file will automatically block secrets.toml)
git add .

# 3. Write a crisp, descriptive commit message following professional naming conventions
git commit -m "docs: implement comprehensive architecture diagram and rewrite project README"

# 4. Safely pull down any remote updates to prevent branching conflicts
git pull origin main --rebase

# 5. Securely dispatch your local codebase updates to your live production repo
git push origin main
