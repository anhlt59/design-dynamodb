from app.common.constants import APP_HOST, APP_PORT
from app.framework.bootstrap import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
