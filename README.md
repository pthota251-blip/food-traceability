# SafeTrace: Advanced AI Food Contamination Traceability & Real-Time Recall System

An enterprise-grade, hackathon-ready food safety and traceability platform engineered with **React**, **Python FastAPI**, and **MySQL**. Provides cryptographic QR provenance tracing, computer-vision contamination screening, IoT cold-chain thermal anomaly detection, and real-time emergency recall broadcasts via WebSockets.

---

## 1. System Architecture & Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons, Recharts, HTML5-QRCode scanner, QRcode.react.
- **Backend**: Python 3.10+ FastAPI, SQLAlchemy 2.0, PyMySQL, Pydantic v2, Python-Jose (JWT), WebSockets.
- **Database**: MySQL (with automatic SQLite fallback for rapid local test development).
- **AI/ML Layer**: Computer Vision spoilage detection & Multi-sensor cold-chain risk heuristic analyzer.

---

## 2. Directory Structure & File Purpose Guide

```
food-contamination-traceability/
├── backend/                               # Python FastAPI backend application
│   ├── app/
│   │   ├── __init__.py                    # Backend application package marker
│   │   ├── main.py                        # FastAPI application entrypoint, CORS & static file mount
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py                  # Pydantic environment configuration (.env loader)
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                    # SQLAlchemy Declarative Base
│   │   │   ├── session.py                 # MySQL engine, connection pool, and get_db session dependency
│   │   │   └── init_db.py                 # Table creation runner & metadata sync
│   │   ├── models/                        # Relational database models
│   │   │   ├── __init__.py                # Model exports & metadata aggregator
│   │   │   ├── user.py                    # User entity with roles (Farmer, Admin, Inspector, etc.)
│   │   │   ├── batch.py                   # Product batch entity with cryptographic provenance hash
│   │   │   ├── checkpoint.py              # Chain-of-custody transfer checkpoints
│   │   │   ├── telemetry.py               # IoT sensor logs (temperature, humidity, cold chain breaches)
│   │   │   ├── inspection.py              # AI visual contamination inspection results
│   │   │   ├── report.py                  # Consumer and inspector incident reports
│   │   │   └── recall.py                  # Emergency recall & alert records
│   │   └── api/
│   │       ├── __init__.py
│   │       └── v1/
│   │           ├── __init__.py
│   │           └── api.py                 # Router aggregator & healthcheck
│   ├── .env.example                       # Backend environment variable template
│   ├── .env                               # Active backend configuration
│   ├── init_db.sql                        # MySQL database creation script
│   └── requirements.txt                   # Backend Python dependencies
│
├── frontend/                              # Modern React frontend application
│   ├── public/                            # Static public web assets
│   ├── src/
│   │   ├── assets/                        # Images, logos, and graphic assets
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Navbar.jsx             # Sticky top navigation bar
│   │   │   │   ├── Footer.jsx             # System information footer
│   │   │   │   └── AlertBanner.jsx        # Real-time pulsing emergency recall banner
│   │   │   └── layout/
│   │   │       └── MainLayout.jsx         # App shell layout wrapper
│   │   ├── context/
│   │   │   ├── AuthContext.jsx            # Authentication state & role session
│   │   │   └── AlertContext.jsx           # Real-time WebSocket contamination alert state
│   │   ├── pages/
│   │   │   ├── Home.jsx                   # Modern hero landing page with quick batch verification
│   │   │   ├── ScanQR.jsx                 # Live camera & image file QR code scanner
│   │   │   ├── VerifyBatch.jsx            # Provenance timeline, cold chain stats & safety grade
│   │   │   ├── ReportContamination.jsx    # Whistleblower/consumer incident reporting with photo upload
│   │   │   ├── Dashboard.jsx              # Supply chain command center & emergency recall trigger
│   │   │   └── Login.jsx                  # Role preset portal (Farmer, Processor, Retailer, Admin)
│   │   ├── services/
│   │   │   ├── api.js                     # Axios HTTP client with JWT interceptor
│   │   │   └── websocket.js               # Real-time WebSocket connection client
│   │   ├── App.jsx                        # React Router route registry
│   │   ├── index.css                      # Tailwind CSS directives & theme fonts
│   │   └── main.jsx                       # React DOM root render
│   ├── .env.example                       # Frontend environment variable template
│   ├── .env                               # Active frontend configuration
│   ├── index.html                         # Single Page Application HTML root
│   ├── package.json                       # Frontend dependencies & scripts
│   ├── postcss.config.js                  # PostCSS Tailwind processor
│   ├── tailwind.config.js                 # Tailwind CSS custom themes & hazard color palette
│   └── vite.config.js                     # Vite build & dev-server configuration
│
└── README.md                              # Complete system manual & execution instructions
```

---

## 3. Installation & Execution Guide

### Prerequisites
- **Python**: 3.10+ (Verified Python 3.12 installed)
- **Node.js**: v18+ (Verified Node v23 installed)
- **MySQL Server**: (e.g. MySQL 8.0, XAMPP, or Docker)

---

### Step 1: Database Setup (MySQL)

1. Open your MySQL client (MySQL CLI, MySQL Workbench, or phpMyAdmin) and run:
   ```sql
   CREATE DATABASE IF NOT EXISTS food_traceability_db
       CHARACTER SET utf8mb4
       COLLATE utf8mb4_unicode_ci;
   ```
   *(Or execute `mysql -u root -p < backend/init_db.sql`)*

2. In `backend/.env`, verify your MySQL credentials:
   ```env
   DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/food_traceability_db
   ```
   *Note: If MySQL is not running yet during initial testing, `ENABLE_SQLITE_FALLBACK=true` allows the application to run seamlessly on SQLite until MySQL is ready.*

---

### Step 2: Backend Installation & Startup

1. Open a terminal in the `backend` folder:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```powershell
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   - **Interactive API Documentation (Swagger)**: http://localhost:8000/api/v1/docs
   - **Alternative ReDoc Docs**: http://localhost:8000/api/v1/redoc
   - **Health Check**: http://localhost:8000/api/v1/health

---

### Step 3: Frontend Installation & Startup

1. Open a new terminal in the `frontend` folder:
   ```bash
   cd frontend
   ```

2. Install npm packages:
   ```bash
   npm install
   ```

3. Start the Vite React development server:
   ```bash
   npm run dev
   ```
   - **Web Application URL**: http://localhost:5173

---

## 4. Phase 1 Verification Checklist

- [x] React frontend structure initialized with Tailwind CSS, Vite, Lucide Icons, and React Router.
- [x] Python FastAPI backend application architecture constructed with settings management.
- [x] MySQL database connection configured with connection pooling (`pool_pre_ping`, `pool_recycle`).
- [x] Initial 7 relational database models defined with relationships, foreign keys, and indexes:
  - `User` (RBAC)
  - `Batch` (Lot tracing & provenance hash)
  - `SupplyChainCheckpoint` (Handoff locations & actions)
  - `EnvironmentalTelemetry` (IoT temp & humidity breaches)
  - `AIInspection` (Visual spoilage & defect classification)
  - `ContaminationReport` (Public incident & whistleblower filings)
  - `RecallAlert` (Class I-III emergency recall declarations)
- [x] `requirements.txt` and `package.json` created with production dependencies.
- [x] Detailed documentation and step-by-step setup instructions provided.

