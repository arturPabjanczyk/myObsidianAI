#!/usr/bin/env bash
set -euo pipefail

# lokalne testy: wszystko w katalogu projektu
DATA_DIR="${DATA_DIR:-.}"
CHROMA_DIR="${DATA_DIR}/chroma_db"
DOCS_DIR="${DATA_DIR}/docs"

# lokalne testy: stały port
PORT="${PORT:-8000}"

if [ "${FORCE_INGEST:-0}" = "1" ]; then
  echo "[start] FORCE_INGEST=1 -> running ingest"
  python ingest.py
elif [ ! -d "${CHROMA_DIR}" ] || [ -z "$(ls -A "${CHROMA_DIR}" 2>/dev/null || true)" ]; then
  echo "[start] chroma_db empty -> running ingest"
  mkdir -p "${DOCS_DIR}"
  python ingest.py
else
  echo "[start] chroma_db exists -> skip ingest"
fi

exec chainlit run app.py --host 0.0.0.0 --port "${PORT}"