import uvicorn
from bootstrap import app
from entrypoints.fastapi import ApiFactory

api_factory = ApiFactory()
api = api_factory.create(application=app)

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000, type=int)
    args = parser.parse_args()
    port = args.port
    uvicorn.run(api, host="0.0.0.0", port=port)
