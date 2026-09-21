# Infinite Canvas migration

Qwen Canvas is migrating its frontend to basketikun/infinite-canvas while keeping the existing local Qwen-Image-2.1 Python backend and model files.

## Phase 1
Run `安装新版无限画布.bat`. It clones the upstream project into `qwen-canvas/infinite-canvas` and installs the web dependencies. The existing `models/`, `.env`, `outputs/`, `projects/`, and Python backend are not replaced.

## Local integration contract
- Qwen backend: `http://127.0.0.1:8000`
- health: `GET /api/health`
- generation/edit: `POST /api/generate` multipart form
- output: `GET /api/output/{name}`
- image edit supports up to 10 reference images.

## Target interaction
The mature infinite-canvas frontend becomes the canvas shell. Local Qwen-Image-2.1 remains the default image engine. Cloud providers remain optional.
