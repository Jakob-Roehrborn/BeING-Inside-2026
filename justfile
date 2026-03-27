install:
    just install-be
    just install-fe

install-be:
    cd backend && \
    python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install -r requirements.txt

install-fe:
    cd frontend/ && \
    npm install

dev:
    just dev-be &
    just dev-fe

dev-be:
    cd backend && \
    python3 -m flask run --host 0.0.0.0

dev-fe:
    cd frontend && \
    npm run dev

prod:
    just prod-be
    just prod-fe

prod-be:
    cd backend && nohup gunicorn -b 127.0.0.1:8000 app:app > be.log 2>&1 &

prod-fe:
    cd frontend && npm run build && nohup PORT=3000 HOST=127.0.0.1 node .output/server/index.mjs > be.log 2>&1 & 