import logging
from datetime import datetime
import os 


LOG_FILE = f"log_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(),"logs")
os.makedirs("logs",exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)
    
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    logging.info("Logging has started")