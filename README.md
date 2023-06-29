# FastAPI authentication with JWT token

```bash
# active virtual environment
python -m venv .venv
source .venv/bin/activate

# install dependencies (FastAPI)
pip install -e .

# run server
uvicorn demo.app:app --reload
```

1. Go to http://127.0.0.1:8000/docs
2. Click padlock next to `/users/me` and try the endpoint out with username `foo` with password `bar`.
