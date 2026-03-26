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