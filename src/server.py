import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.requests import Request
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.threading import ThreadingIntegration
import logging

from src.routers.server import router
from src.schemas.basic import TextOnly
from src.utils.swagger import custom_swagger_ui_html

# Initialize Sentry
sentry_dsn = os.environ.get("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        send_default_pii=True,
        environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
        traces_sample_rate=float(os.environ.get("SENTRY_TRACES_SAMPLE_RATE", "1.0")),
        profiles_sample_rate=float(os.environ.get("SENTRY_PROFILES_SAMPLE_RATE", "1.0")),
        enable_tracing=True,
        enable_logs=True,
        profile_lifecycle="trace",
        integrations=[
            # FastAPI Integration - captures request/response data and errors
            FastApiIntegration(
                transaction_style="endpoint",  # Use endpoint name as transaction name
                failed_request_status_codes=[range(500, 599)],  # Track 500 and 5xx as failed
            ),
            # Starlette Integration - for low-level ASGI framework support
            StarletteIntegration(
                transaction_style="endpoint",
                failed_request_status_codes=[range(500, 599)],  # Track 500 and 5xx as failed
            ),
            # Logging Integration - captures logs and sends to Sentry
            LoggingIntegration(
                level=logging.INFO,  # Capture INFO and above as breadcrumbs
                event_level=logging.ERROR,  # Send ERROR and above as events
            ),
            # Redis Integration - tracks Redis operations and performance
            RedisIntegration(),
            # SQLAlchemy Integration - tracks database queries and performance
            SqlalchemyIntegration(),
            # Threading Integration - tracks errors in threads
            ThreadingIntegration(propagate_hub=True),
        ],
        # Additional options
        attach_stacktrace=True,  # Attach stack traces to messages
        send_client_reports=True,  # Send client error reports
        max_breadcrumbs=100,  # Maximum number of breadcrumbs
        debug=False,  # Set to True for debug output
        before_send=lambda event, hint: event,  # Hook to modify events before sending
    )

app = FastAPI(
    title="Template FastAPI Backend Server",
    description="Template Description",
    version="0.0.1",
    contact={
        "name": "Author Name",
        "email": "example@exmaple.com",
    },
    docs_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/docs", include_in_schema=False)
async def custom_docs():
    return custom_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={'docExpansion': 'none'}
    )


@app.get("/", response_model=TextOnly)
async def root():
    return TextOnly(text="Hello World")


@app.get("/elements", include_in_schema=False)
async def api_documentation(request: Request):
    return HTMLResponse("""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Elements in HTML</title>

    <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
  </head>
  <body>

    <elements-api
      apiDescriptionUrl="openapi.json"
      router="hash"
    />

  </body>
</html>""")
