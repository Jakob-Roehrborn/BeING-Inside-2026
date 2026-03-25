install:
    just install-backend
    just install-frontend

install-backend:
    cd backend && \
    python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install -r requirements.txt

install-frontend:
    cd frontend/ && \
    npm install

run:
    just run-frontend &
    just run-backend

run-backend:
    cd backend && \
    python3 -m flask run

run-frontend:
    cd frontend && \
    npm run dev