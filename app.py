from src.bootstrap import create_app
from src.config import APP_HOST, APP_PORT

app = create_app()


@app.route("/health")
def health():
    return '{"status":true}', 200


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
