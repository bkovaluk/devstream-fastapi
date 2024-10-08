# app/core/utils/logging.py

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ],
)

logger = logging.getLogger(__name__)
