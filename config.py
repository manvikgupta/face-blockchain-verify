import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SCRAPE_DO_API_KEY = os.getenv("SCRAPE_DO_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
WEB3_RPC_URL = os.getenv("WEB3_RPC_URL", "http://127.0.0.1:8545")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
NETWORK = os.getenv("NETWORK", "local")