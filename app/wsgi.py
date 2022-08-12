from entrypoints.api import flask_app

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000, type=int)
    args = parser.parse_args()
    port = args.port

    flask_app.run(debug=True, host="0.0.0.0", port=port)
