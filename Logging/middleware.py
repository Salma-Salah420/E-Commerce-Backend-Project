import time
from fastapi import Request
from logging.logger import logger

async def log_requests(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    logger.info(
        f"{request.method} {request.url.path} "
        f"Status={response.status_code} "
        f"Time={duration:.2f}s"
    )

    return response
