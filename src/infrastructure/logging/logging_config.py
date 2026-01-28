import logging

def setup_logging(path : str = "bank.log"):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(path),
            logging.StreamHandler()
        ]
    )

