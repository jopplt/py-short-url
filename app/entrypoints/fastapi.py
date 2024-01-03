import pydantic
from application import main
from application.ports import errors, requests, responses
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response


class EncodeRequest(pydantic.BaseModel):
    url: pydantic.HttpUrl


class ApiFactory:
    @classmethod
    def create(cls, application: main.App) -> FastAPI:
        fast_api = FastAPI()

        @fast_api.get(
            "/", include_in_schema=False, status_code=200, response_class=Response
        )
        def home() -> Response:  # pragma: no cover
            return Response(
                content="""
            <h1>URL Shortener</h1>
            <p>Find the api docs <a href=\"/docs/\">here</a>.</p>
            """,
                media_type="text/html",
            )

        @fast_api.get("/favicon.ico", include_in_schema=False, status_code=204)
        def favicon() -> None:  # pragma: no cover
            return None

        @fast_api.put(
            "/encode", response_model=str, status_code=200, response_class=Response
        )
        def encode(request: EncodeRequest) -> Response:
            """Encode
            Returns a short code for a given URL
            ---
            parameters:
              - in: body
                name: body
                required: true
                schema:
                  type: object
                  properties:
                    url:
                      type: string
                      example: https://google.com
                  required:
                    - url
            responses:
              200:
                description: Short code for the original URL
                schema:
                  type: string
            """
            try:
                response = application.handle(requests.EncodeUrl(url=str(request.url)))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            try:
                assert isinstance(response, responses.EncodedUrl)
                return Response(content=response.code, media_type="text/plain")
            except AssertionError as e:
                raise HTTPException(status_code=500, detail=str(e))

        @fast_api.get(
            "/decode/{code}",
            response_model=str,
            status_code=200,
            response_class=Response,
        )
        def decode(code: str) -> Response:
            """Decode
            Returns the original URL given a short code
            ---
            parameters:
              - in: path
                name: code
                required: true
                schema:
                  type: string
                  example: bqrvjs
            responses:
              200:
                description: Decoded URL
                schema:
                  type: string
              404:
                description: Not found - URL was not encoded
            """
            try:
                response = application.handle(requests.DecodeShortenedUrl(code=code))
            except errors.UrlNotFound as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

            if isinstance(response, responses.DecodedUrl):
                return Response(content=response.url, media_type="text/plain")

            raise HTTPException(status_code=500, detail="Internal server error")

        return fast_api
