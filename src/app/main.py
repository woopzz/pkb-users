from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.core.config import settings
from app.router import router

app = FastAPI(
    title='Users API',
    summary='Manage users. Handle authentication.',
    version='1.0.0',
)
app.add_middleware(PrometheusMiddleware, skip_paths=['/metrics'])
app.add_route('/metrics', handle_metrics)
app.include_router(router, prefix=settings.API_V1_STR)


@app.get('/healthcheck', include_in_schema=False)
def healthcheck():
    return {'status': 'ok'}
