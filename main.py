from fastapi import FastAPI
import logging
from utils.logger import setup_logging 

setup_logging()
logger = logging.getLogger('my_module')

app = FastAPI()

@app.get("/")
def read_root():

    logger.info("/ reached")
    logger.debug("hello")
    logger.error("err")
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    logger.info("/items/{" + str(item_id) + "}")
    return {"item_id": item_id, "q": q}

