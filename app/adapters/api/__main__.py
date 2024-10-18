from app.adapters.api.bootstrap import create_app
from app.common.configs import HOST, PORT

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.adapters.api.__main__:app", host=HOST, port=PORT, reload=True, reload_dirs=["app"])
