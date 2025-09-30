import logging
import sys

def setup_logger():
    """
    Sets up a centralized logger for the application.
    """
    # Create a logger
    logger = logging.getLogger("ContentGrinder")
    logger.setLevel(logging.INFO)

    # Create a handler to write logs to the console (stdout)
    handler = logging.StreamHandler(sys.stdout)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        logger.addHandler(handler)

    # Enable debug logging for Google API client libraries to see detailed OAuth flow.
    # This will print detailed information about the requests/responses during authentication.
    logging.getLogger('google_auth_oauthlib').setLevel(logging.INFO)
    logging.getLogger('googleapiclient').setLevel(logging.INFO)

    return logger

# Create a single instance of the logger to be used across the application
log = setup_logger()