#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${DATA_DIR:-/data}"
CHROMA_DIR="${DATA_DIR}/chroma_db"
PORT="${PORT:?PORT is required on Railway}"

if [ "${FORCE_INGEST:-0}" = "1" ]; then
  echo "[start] FORCE_INGEST=1 -> ingest"
  python ingest.py
elif [ ! -d "${CHROMA_DIR}" ] || [ -z "$(ls -A "${CHROMA_DIR}" 2>/dev/null || true)" ]; then
  echo "[start] chroma_db empty -> ingest"
  python ingest.py
else
  echo "[start] chroma_db exists -> skip ingest"
fi

exec chainlit run app.py --host 0.0.0.0 --port "${PORT}"