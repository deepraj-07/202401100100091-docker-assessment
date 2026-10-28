# FestPass 2026 — Docker & Container Security Assessment (CA-2)

A three-tier FestPass registration application built and validated as part of the Docker & Container Security CA-2 practical. The project demonstrates containerization, Docker Compose networking, persistent storage, image vulnerability scanning, registry publishing, and image signing with Cosign.

## 1. Candidate Details

- **Name:** Deep Raj
- **Registration Number (REGNO):** `202401100100091`
- **Published Port:** `8091`
- **Docker Hub Username:** `deepraj07`
- **Docker Hub Repository:** [deepraj07/fest-backend](https://hub.docker.com/r/deepraj07/fest-backend)
- **GitHub Repository:** [202401100100091-docker-assessment](https://github.com/deepraj-07/202401100100091-docker-assessment)

## 2. Project Architecture

The application consists of three services:

- **Frontend:** Nginx serves the FestPass registration interface.
- **Backend:** A Python Flask API handles health checks and registration requests.
- **Database:** PostgreSQL stores registration records persistently.

Docker Compose manages the services, networks, and persistent database volume.

### Network Isolation

Two separate Docker networks are configured:

- `frontend-facing`: connects the frontend and backend.
- `database-facing`: connects the backend and PostgreSQL database.

The frontend is not attached to the database-facing network. Consequently, the frontend cannot resolve the database service name directly through Docker's internal DNS.

### Persistent Storage

PostgreSQL uses the named volume:

`202401100100091-docker-assessment_postgres-data`

This volume retains database records when containers are removed and recreated using `docker compose down` followed by `docker compose up -d`.

## 3. Run the Application

### Prerequisites

- Docker Desktop with Docker Compose
- A local `.env` file containing the required PostgreSQL configuration

### Startup

1. Create `.env` from `.env.example` and configure a local PostgreSQL password.
2. Start the application:

   ```powershell
   docker compose up -d
   ```

3. Check the running services:

   ```powershell
   docker compose ps
   ```

4. Open the frontend:

   `http://localhost:8091`

5. Check backend health:

   ```powershell
   Invoke-RestMethod http://localhost:8091/api/health
   ```

6. Stop the services:

   ```powershell
   docker compose down
   ```

The named PostgreSQL volume is retained unless explicitly removed.

**Security note:** `.env`, private signing keys, Docker Hub passwords, and access tokens must remain outside Git commits.

## 4. Validation Results

Validation was performed locally on 28 October 2026.

- The backend health endpoint returned registration number `202401100100091`, version `0.1` for the Stage 1 test, and `database: false` when PostgreSQL was not available to the standalone backend.
- The frontend could not resolve the database service name from its network. The attempted `ping -c 1 db` failed with `bad address 'db'`.
- Three registrations—`Asha - Hackathon`, `Ravi - Robotics`, and `PersistenceCheck - SecurityLab`—were present after a Compose restart.
- The named PostgreSQL volume remained available after the containers were recreated.
- The published registry image `deepraj07/fest-backend:1.0.0` ran with application version `1.0.0` and displayed the persisted registrations.

## 5. Image Vulnerability Assessment

Trivy was used to compare the initial backend image with the hardened image.

| Image | CRITICAL vulnerabilities | HIGH vulnerabilities | Image size |
|---|---:|---:|---:|
| `fest-backend:0.1` — before hardening | 9 | 92 | 199,079,280 bytes |
| `fest-backend:0.2` — after hardening | 2 | 59 | 269,412,022 bytes |

The hardened image reduced the reported CRITICAL and HIGH vulnerability counts. Its measured image size increased; hardening did not reduce the image size in this build.

### Required CRITICAL Vulnerability Gate

The following command was executed:

```powershell
trivy image --severity CRITICAL --ignore-unfixed --exit-code 1 fest-backend:0.2
```

The command returned exit code `0`, indicating that no vulnerabilities matching the selected CRITICAL severity and `--ignore-unfixed` filter caused the gate to fail.

This filtered gate result should be distinguished from the full before-and-after vulnerability totals in the table.

The Trivy reports are retained in the `reports/` directory.

## 6. Docker Hub Publishing

The backend image was published to [Docker Hub](https://hub.docker.com/r/deepraj07/fest-backend).

### Release Tags

The following tags were published for the signed release:

- `deepraj07/fest-backend:1.0.0`
- `deepraj07/fest-backend:1.0`
- `deepraj07/fest-backend:latest`

The registry inspection confirmed the following immutable digest for version `1.0.0`:

`sha256:04bede43b848626be9a222beddb9d9de807788691789f662737e890cfb5d3610`

The `1.0`, `1.0.0`, and `latest` tags were checked against Docker Hub and resolved to the same release digest.

### Unsigned Release

Version `1.0.1` was also published for the signature-verification test.

Its digest was:

`sha256:8f4ade0057da3b59dffe246c2c0e2b66e5bb50adc5108cb8d10d62b5ac0eb9de`

This release was intentionally left unsigned to test rejection by Cosign verification.

## 7. Cosign Image Signing and Verification

Cosign `v3.1.4` was used to sign and verify container images.

- A local Cosign key pair was generated.
- The private key `cosign.key` is ignored by Git and must not be committed.
- The public key `cosign.pub` is retained for verification.
- The `1.0.0` image was signed by its immutable digest.
- Verification of the `1.0.0` digest using `cosign.pub` succeeded.
- Verification of the unsigned `1.0.1` digest failed with `no signatures found` and exit code `10`.

The signing and verification results demonstrate the distinction between a signed release and an unsigned release.

## 8. Assessment Evidence

Terminal and browser screenshots are stored in the `screenshots/` directory. They document image builds, health checks, frontend registrations, network isolation, persistence, vulnerability scans, Docker Hub publishing, and Cosign operations.

The screenshot filenames currently use descriptive names. Before final submission, compare them with the assessment's required evidence codes to ensure that every required item can be identified easily.

## 9. AI Tools and Assistance Disclosure

### GitHub Copilot

GitHub Copilot was used in VS Code to assist with:

- Generating and refining Dockerfiles for the backend and frontend.
- Creating and reviewing `compose.yaml`, including services, networks, and persistent storage.
- Suggesting command sequences for image builds, vulnerability scans, registry publishing, and Cosign signing and verification.
- Drafting and refining project documentation.
- Debugging errors encountered during implementation, including Cosign execution issues and terminal/prompt configuration.

### ChatGPT

ChatGPT was used to explain Docker and container-security concepts, review command output, troubleshoot errors, guide evidence capture, and refine the README and submission workflow.

**Execution responsibility:** I ran the commands myself on my own machine, inspected the resulting outputs, and performed the validation steps. AI tools assisted with implementation, explanation, and debugging.

## 10. Outstanding Evidence and Submission Checks

- Confirm that the `S1-2` screenshot clearly documents the genuine Stage 1 build using `FROM python:3.9`.
- Capture a dedicated `S5-2` screenshot showing the successful Cosign signing command and its result.
- Verify that every required assessment screenshot is present, legible, and identifiable by its required evidence code.
- Confirm that the GitHub repository and Docker Hub repository are public.
- Ensure that `cosign.key`, `.env`, Docker Hub passwords, and access tokens are absent from all Git commits.
- Confirm that the `1.0.0` release is signed and the `1.0.1` test release remains unsigned.

## 11. Repository Structure

```text
202401100100091-docker-assessment/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   └── nginx.conf
├── reports/
│   ├── trivy-before.txt
│   └── trivy-after.txt
├── screenshots/
├── .env.example
├── .gitignore
├── compose.yaml
└── README.md
```

The local `.env` file and private Cosign key are intentionally excluded from version control.
