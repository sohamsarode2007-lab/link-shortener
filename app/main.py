from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.shortener import Shortener, ShortenerError

app = FastAPI(title="Link Shortener")
shortener = Shortener()


class ShortenRequest(BaseModel):
    url: str


@app.post("/shorten", status_code=201)
def shorten(body: ShortenRequest) -> dict[str, str]:
    try:
        return {"code": shortener.shorten(body.url)}
    except ShortenerError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/{code}")
def follow(code: str) -> RedirectResponse:
    try:
        return RedirectResponse(shortener.resolve(code))
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown short code") from None
