from fastapi import FastAPI

from app.core.config import settings
from app.router import router

app = FastAPI(
    title='Users API',
    summary='Manage users. Handle authentication.',
    version='1.0.0',
)
app.include_router(router, prefix=settings.API_V1_STR)


@app.get('/healthcheck', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app=app,
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        workers=settings.UVICORN_WORKERS,
    )
