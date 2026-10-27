import logging

from fastapi import Request
import time
import uuid


logger = logging.getLogger(__name__)


# async def log_requests(request: Request, call_next):
#     # Before FastAPI handles the request:
#     logger.info(f"Received: {request.method} {request.url.path}")

#     # FastAPI handles the request
#     response = await call_next(request)

#     # After FastAPI produces a response:
#     logger.info(f"Returned: status={response.status_code}")
#     return response


async def log_requests(request: Request, call_next):
    # Before: identify the request and start the timer.
    request_id = uuid.uuid4().hex[:8]
    request.state.request_id = request_id
    started = time.perf_counter()

    response = await call_next(request)

    # After: measure, log, and attach the response header.
    duration_ms = (time.perf_counter() - started) * 1000
    logger.info(f"request_id={request_id} {request.method} {request.url.path} status={response.status_code} duration={duration_ms:.1f}ms")
    response.headers["X-Request-ID"] = request_id
    return response



