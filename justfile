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
    python3 -m flask run

dev-fe:
    cd frontend && \
    npm run dev

prod-be:
    cd backend && \
    gunicorn -b 127.0.0.1:8000 app:app

prod-fe:
    cd frontend && \
    npm run build && \
    PORT=3000 HOST=127.0.0.1 node .output/server/index.mjs