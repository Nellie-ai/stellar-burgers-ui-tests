import os


BASE_URL = os.getenv(
    "STELLAR_BURGERS_URL", "https://stellarburgers.education-services.ru"
)
API_URL = os.getenv("STELLAR_BURGERS_API_URL", BASE_URL)
DEFAULT_TIMEOUT = int(os.getenv("SELENIUM_TIMEOUT", "15"))
ORDER_TIMEOUT = int(os.getenv("ORDER_TIMEOUT", "180"))
