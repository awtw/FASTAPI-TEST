import logging
from fastapi import APIRouter
import sentry_sdk

from src.utils.utils import wrap_logger

router = APIRouter()
logger = logging.getLogger(__name__)
wrap_logger(logger)


@router.get("/test-sentry-error")
async def test_sentry_error():
    """
    Test endpoint to trigger an error and verify Sentry error tracking.
    This error will be captured and sent to Sentry.
    """
    logger.info("Testing Sentry error tracking endpoint")
    raise ValueError("This is a test error for Sentry - if you see this in Sentry, it's working!")


@router.get("/test-sentry-logging")
async def test_sentry_logging():
    """
    Test endpoint to verify Sentry logging integration.
    Check your Sentry dashboard for the error log.
    """
    logger.info("This is an INFO log - will appear as breadcrumb in Sentry")
    logger.warning("This is a WARNING log - will appear as breadcrumb in Sentry")
    logger.error("This is an ERROR log - will be sent to Sentry as an event")
    
    return {
        "status": "success",
        "message": "Check your Sentry dashboard - the ERROR log should appear there"
    }


@router.get("/test-sentry-capture")
async def test_sentry_capture():
    """
    Test endpoint to manually capture a message in Sentry.
    """
    sentry_sdk.capture_message("Manual Sentry test message", level="info")
    
    return {
        "status": "success", 
        "message": "Manual message sent to Sentry"
    }
