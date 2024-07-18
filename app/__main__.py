from app.core.bootstrap import create_app
from app.core.config import APP_HOST, APP_PORT

app = create_app()

if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
