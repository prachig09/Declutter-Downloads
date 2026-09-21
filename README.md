# Declutter Downloads – File Sorter

An automated, cross-platform background file-organization daemon built with Python 3.13, dynamic tag-based routing, real-time Prometheus telemetry, and robust multi-OS CI/CD pipelines.

---

## Purpose

Downloads folders across operating systems quickly become cluttered dumps of unnamed or mixed files. Manual organization is tedious and easy to neglect. 

**Declutter Downloads** solves this by running silently in the background, intercepting incoming files in real time, matching them against tag rules, and routing them to target directory structures—all without interrupting your workflow or processing incomplete/temporary downloads.

---

## Architecture & Methodology

* **Event-Driven File Traversal:** Uses `watchdog`'s `PollingObserver` to monitor file creation events reliably across both native OS filesystems and mounted paths (such as Windows drives mounted inside WSL `/mnt/c/`).
* **Non-Blocking Logic & Safety First:**
  * **Temporary File Protection:** Bypasses active downloads (`.crdownload`, `.tmp`, `.part`) and hidden system files to prevent corrupting in-flight transfers.
  * **Resilient I/O:** Uses `shutil.move` with explicit `OSError` exception handling to ensure filesystem errors never crash the daemon.
* **Observability First:** Integrates `prometheus_client` to expose operational telemetry at `http://localhost:8000/metrics` tracking total files organized, failures, latencies, and unmatched items.
* **Rigorous CI/CD Matrix:** Runs automated testing across **Ubuntu, macOS, and Windows** on **Python 3.10, 3.11, and 3.12** using GitHub Actions, enforced with `ruff` linting and `pytest` test suites.
* **Headless Deployment:** Fully Dockerized with `docker-compose` for lightweight, containerized background execution.

---

## Tech Stack

| Category | Technology |
|---|---|
| **Core Language** | Python 3.13+ |
| **File Monitoring** | `watchdog` (PollingObserver) |
| **Telemetry & Metrics** | `prometheus_client` |
| **Testing & Quality** | `pytest`, `pytest-cov`, `ruff` |
| **Containerization** | Docker, Docker Compose |
| **CI/CD Pipeline** | GitHub Actions (9-job OS x Python matrix) |

---

## Project Structure

```text
Declutter_Downloads/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions Multi-OS Matrix Pipeline
├── reports/                   # All metrics result snapshots
├── src/
│   ├── config.py              # Centralized tag routing & environment settings
│   ├── file_handler.py        # File processing logic & movement execution
│   ├── metrics.py             # Prometheus metrics definitions & exporter
│   └── watcher.py             # Watchdog event listener loop & entry point
├── tests/
│   └── test_file_handler.py   # Pytest unit tests for temp detection & rules
├── conftest.py                # Pytest path resolution configuration
├── Dockerfile                 # Alpine-based Python container configuration
├── docker-compose.yml         # Containerized local volume deployment
├── pyproject.toml             # Ruff linter and Pytest settings
├── requirements.txt           # Project dependencies
└── README.md
```

---

## Getting Started

### Prerequisites

* **Python:** Version 3.10 or higher (Python 3.13 recommended)
* **Git:** Installed on your system
* *(Optional)* **Docker & Docker Compose:** Required only if running headlessly inside a container

---

### Option 1: Local / WSL Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/prachig09/Declutter_Downloads.git](https://github.com/prachig09/Declutter_Downloads.git)
   cd Declutter_Downloads
   ```

2. **Create and Activate a Virtual Environment:**

  Linux / macOS / WSL:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

  Windows (PowerShell):
  ```bash
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
3. **Install Dependencies:**
  
  ```bash
  pip install -r requirements.txt
  ```

4. **Configure Your Tag Routing Rules (src/config.py):**

  Open src/config.py and set your watch directory and destination tag mappings:

  ```bash
  WATCH_DIR = "/path/to/your/Downloads"
  
  TAG_RULES = {
      "sem3_": "/path/to/Documents/University/Sem3",
      "tax_": "/path/to/Documents/Finance",
      "work_": "/path/to/Documents/Work",
  }
  
  # Set to True to print planned actions without moving real files
  DRY_RUN = False
  ```

5. **Start the Sorter Daemon:**
  ```bash
  python -m src.watcher
  ```
---

### Option 2: Docker Setup (Headless Execution)

1. **Configure Directory Mounts (docker-compose.yml):**

  ```bash
  services:
    declutter-daemon:
      build: .
      volumes:
        - /path/to/host/Downloads:/data/downloads
        - /path/to/host/Documents:/data/documents
      ports:
        - "8000:8000"
      restart: unless-stopped
  ```

2. **Build and Launch the Container:**

  ```bash
  docker compose up -d --build
  ```
3. **Check Container Logs & Status:**

  ```bash
  docker compose logs -f
  ```

## Telemetry & Metrics

While the daemon is running, scrape or view Prometheus metrics at http://localhost:8000/metrics.

### Exposed Metrics:

1. `files_sorted_total`: Counter tracking sorted files labeled by category and status (success / failed).
2. `unmatched_files_total`: Counter tracking files created that did not match any tag rules.
3. `file_processing_seconds`: Histogram measuring execution latency per file move.

## Running Tests & Quality Checks

  ```bash
  # Code formatting and quality check
  ruff check .
  # Run test suite with coverage report
  python -m pytest --cov=src tests/
  ```
