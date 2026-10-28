# FestPass 2026 Docker & Container Security

Three-tier FestPass registration application for the Docker & Container Security
CA-2 practical.

## Candidate details

- Name: Deepraj
- Registration number: `202401100100091`
- Published port: `8091`
- Docker Hub: [deepraj07/fest-backend](https://hub.docker.com/r/deepraj07/fest-backend)
- GitHub: [202401100100091-docker-assessment](https://github.com/deepraj-07/202401100100091-docker-assessment)

## Run the application

1. Copy `.env.example` to `.env` and set a local PostgreSQL password.
2. Run `docker compose up -d`.
3. Open `http://localhost:8091`.
4. Check the API with `Invoke-RestMethod http://localhost:8091/api/health`.
5. Stop the stack with `docker compose down` (the named database volume is retained).

The final Compose configuration uses two networks: the frontend-facing network
connects Nginx to the backend, while the database-facing network connects the
backend to PostgreSQL. The frontend is not attached to the database network.

## Image security results

| Image | CRITICAL | HIGH | Size |
|---|---:|---:|---:|
| `fest-backend:0.1` before | 9 | 92 | 199,079,280 bytes |
| `fest-backend:0.2` after | 2 | 59 | 269,412,022 bytes |

The required fixed-image gate
`trivy image --severity CRITICAL --ignore-unfixed --exit-code 1 fest-backend:0.2`
returned exit code `0`; its filtered result was 0 CRITICAL and 0 HIGH.

Version `1.0.0` immutable digest: pending Docker Hub push.

## Assessment evidence

Evidence screenshots belong in `screenshots/` and must be captured from the
actual terminal/browser session. The required runtime-dependent evidence is
not fabricated by this repository.

## AI tools

- GitHub Copilot (Copilot SDK in VS Code): used to implement and review the
  Docker, Compose, Flask, Nginx, and documentation files.
- ChatGPT: not used.

## Incomplete tasks

- Capture the required Stage 1 and Stage 2 screenshots.
- Push `1.0.0`, record its actual digest, and update Compose verification evidence.
- Install Cosign, sign `1.0.0`, verify it, and demonstrate unsigned `1.0.1` rejection.
- Capture and retain all required evidence screenshots.