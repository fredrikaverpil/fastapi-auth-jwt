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

1. Run server using uvicorn
1. Go to http://127.0.0.1:8000/docs
1. Try the `/users/me` endpoint out, access is denied.
1. Click padlock next to `/users/me` and log in with username `foo` with password `bar`.
1. Try the `/users/me` endpoint out, access is now granted!
