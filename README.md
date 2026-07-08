# DocShift – Document Utility Workspace

## 📚 Overview
DocShift is a **full‑stack** application that provides a web‑based workspace for converting, merging, splitting, and compressing documents. It consists of:

| Component | Location | Tech stack |
|-----------|----------|------------|
| **Backend API** | `backend/` | FastAPI (Python) |
| **Frontend UI** | `frontend/` | Next.js 14 (React 18) + TypeScript + Tailwind |
| **Shared Types** | `frontend/types/` | TypeScript interfaces mirroring the backend models |
| **Tool Registry** | `backend/app/core/registry.py` | Central registry that maps tool IDs to handler functions |
| **Service Stubs** | `backend/app/services/tools/` | Placeholder handlers that return mock responses (replace with real logic) |

The repository is intentionally lightweight so you can **run it locally** or **containerise** it for production.

---

## ✅ Prerequisites
- **Python 3.12+** (add to `PATH`).
- **Node 20+** and **npm** (add to `PATH`).
- **Git** (optional, for cloning).
- **PowerShell** (default on Windows) or any POSIX‑compatible shell.
- Optional: **Docker** if you want to run the whole stack in containers.

---

## 🛠️ Backend – FastAPI
1. Open a terminal and `cd` into the backend folder:
```powershell
cd C:\Users\ayush\OneDrive\Desktop\docshift\backend
```
2. Create & activate a virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# (or .\.venv\Scripts\activate for cmd.exe)
```
3. Upgrade pip (optional but recommended):
```powershell
python -m pip install --upgrade pip
```
**🔧 Install Python dependencies**
```powershell
python -m pip install -r requirements.txt
```
5. (Optional) Create a `.env` file to override defaults. Example:
```text
UPLOAD_DIR=./_uploads
OUTPUT_DIR=./_outputs
MAX_UPLOAD_MB=100
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```
6. Ensure upload/output directories exist (the app will create them at startup, but you can pre‑create them):
```powershell
mkdir _uploads,_outputs
```
7. Run the API in development mode (auto‑reload on changes):
```powershell
uvicorn app.main:app --reload --port 8000
```
   The API will be reachable at **`http://127.0.0.1:8000`**.

---

## 🌐 Frontend – Next.js
1. Open another terminal (or keep the backend running and open a new tab) and `cd` into the frontend folder:
```powershell
cd C:\Users\ayush\OneDrive\Desktop\docshift\frontend
```
2. Install the npm dependencies (exact versions are locked in `package.json`):
```powershell
npm ci
```
3. Copy the example environment file and edit if you changed the backend host/port:
```powershell
Copy-Item .env.local.example .env.local
notepad .env.local   # optional – set NEXT_PUBLIC_API_URL if needed
```
   By default the frontend expects the API at `http://127.0.0.1:8000`.
4. Start the development server:
```powershell
npm run dev
```
   The UI will be served at **`http://localhost:3000`**. Open that URL in a browser.

---

## 🔄 End‑to‑End Quick Test
1. In the browser, select a tool (e.g., *PDF → Word*).
2. Drag a PDF file onto the drop‑zone.
3. The front‑end will POST the file to `/api/jobs`.
4. You’ll receive a mock result (e.g., `converted.docx`). A **ResultCard** with a download link will appear.

> **Note:** The current back‑end handlers are placeholders (`stub_handler`). To get real conversions, replace the stub in `backend/app/services/tools/<tool>.py` with actual logic (see the analysis message for an example using `pdf2docx`).

---

## 🐳 Run Everything with Docker (optional)
1. Create a `Dockerfile` at the project root (you can copy the sample from the repo’s `README` or the analysis).  A minimal multi‑stage Dockerfile is provided in the repo’s `docker/` folder.
2. Build the image:
```powershell
docker build -t docshift .
```
3. Run the container (exposes API on 8000 and UI on 3000):
```powershell
docker run -d -p 8000:8000 -p 3000:3000 --name docshift docshift
```
4. Visit **`http://localhost:3000`**.

---

## 🛡️ Next Steps / Things to Improve
- Replace the **stub handlers** with real conversion logic (`pdf2docx`, `pypdf`, `python-docx`, etc.).
- Move heavy work to a background task queue (Celery/RQ) and expose a `/api/jobs/{id}` status endpoint.
- Add proper **authentication** (JWT or API‑key) and **rate‑limiting** for production.
- Write unit tests for both backend (`pytest`) and frontend (Jest + React Testing Library).
- Harden file‑upload validation (type, size, path sanitisation).
- Deploy behind a TLS terminator (NGINX, Cloudflare) for secure HTTPS traffic.

---

## 📞 Need Help?
If you run into any issues, feel free to open an issue in the repository or reach out to the maintainer.

Happy coding! 🎉