import logging

# Initialize logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER: logging.Logger = logging.getLogger(__name__)
