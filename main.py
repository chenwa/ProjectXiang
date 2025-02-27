from fastapi import FastAPI
import logging


def setup_logger(log_file):
    logger = logging.getLogger("MyLogger")
    logger.setLevel(logging.DEBUG)
    # Create a file handler to write logs to a file
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    # Create a console handler to output logs to the console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # Create a formatter to specify the log message format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

app = FastAPI()
logger = setup_logger("logs.log")

@app.get("/")
def read_root():

    logger.info("/ reached")
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    logger.info("/items/{" + str(item_id) + "}")
    return {"item_id": item_id, "q": q}

