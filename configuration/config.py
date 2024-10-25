import os

# Charger les variables d'environnement depuis le fichier .env
# main.py -> load_dotenv('cred.env')

# use a cred.env files to store your api key
print("API Key:", os.getenv("BINANCE_API_KEY"))
print("Secret Key:", os.getenv("BINANCE_SECRET_KEY"))
API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
# Timing pour le recvWindow
RECV_WINDOW=5000

BASE_URLS = [
    'https://api.binance.com',
    'https://api-gcp.binance.com',
    'https://api1.binance.com',
    'https://api2.binance.com',
    'https://api3.binance.com',
    'https://api4.binance.com'
]

# Optionnel : un timeout par défaut pour éviter les longues attentes sur un endpoint dégradé
DEFAULT_TIMEOUT = 5  # secondes
TIMEOUT = 30  # en secondes

MAX_RETRY_TIME=120
RETRIES=3

# Configuration Binance API
API='/api/v3'
ENDPOINTS = {
    "new_order_test": f"{API}/order/test",
    "query_order": f"{API}/order",
    "cancel_order": f"{API}/order",
    "cancel_all_orders": f"{API}/openOrders",
    "cancel_replace_order": f"{API}/order/cancelReplace",
    "current_open_orders": f"{API}/openOrders",
    "all_orders": f"{API}/allOrders",
    "new_oco_order": f"{API}/order/oco",
    "new_oto_order": f"{API}/orderList/oto",
    "new_otoco_order": f"{API}/orderList/otoco",
    "cancel_order_list": f"{API}/orderList",
    "query_order_list": f"{API}/orderList",
    "query_all_order_lists": f"{API}/allOrderList",
    "query_open_order_lists": f"{API}/openOrderList",
    "new_sor_order": f"{API}/sor/order",
    "test_sor_order": f"{API}/sor/order/test",
    "account_info": f"{API}/account",
    "account_trades": f"{API}/myTrades",
    "unfilled_order_count": f"{API}/rateLimit/order",
    "prevented_matches": f"{API}/myPreventedMatches",
    "allocations": f"{API}/myAllocations",
    "commission_rates": f"{API}/account/commission",
    "start_user_data_stream": f"{API}/userDataStream",
    "keepalive_user_data_stream": f"{API}/userDataStream",
    "close_user_data_stream": f"{API}/userDataStream",
    "current_price": f"{API}/ticker/price",
    "test_endpoint": f"test_endpoint/test_endpoint"
}