from fastapi import FastAPI

from app.core.config import settings
from app.middlewares.metrics import MetricsMiddleware, metrics_route
from app.router import router

app = FastAPI(
    title=settings.APP_NAME,
    summary='Manage users. Handle authentication.',
    version='1.0.0',
)

app.add_middleware(MetricsMiddleware)
app.add_route('/metrics', metrics_route, include_in_schema=False)

app.include_router(router, prefix=settings.API_V1_STR)


@app.get('/healthcheck', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}
