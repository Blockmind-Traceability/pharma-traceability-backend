import requests
from .models import BlockchainEvent, GenesisBlock
from .exceptions import BlockchainAPIError

BASE_URL = "https://blockchain-connection-production.up.railway.app/api"  

def create_genesis_block(data: GenesisBlock):
    response = requests.post(f"{BASE_URL}/genesis", json=data.__dict__)
    if not response.ok:
        raise BlockchainAPIError("Error creando bloque génesis", response)
    return response.json()

def register_event(event: BlockchainEvent):
    payload = event.__dict__.copy()
    payload["responsible"] = event.responsible.__dict__
    payload["geolocation"] = event.geolocation.__dict__

    response = requests.post(f"{BASE_URL}/events", json=payload)
    if response.status_code != 200:
        raise BlockchainAPIError("Error registrando evento", response)
    return response.json()

def get_blockchain_by_lab(lab_id: str):
    response = requests.get(f"{BASE_URL}/blocks/{lab_id}")
    if response.status_code != 200:
        raise BlockchainAPIError("Error obteniendo blockchain por laboratorio", response)
    return response.json()

def trace_product(lab_id: str, product_serial: str):
    response = requests.get(f"{BASE_URL}/trace/{lab_id}/{product_serial}")
    if response.status_code != 200:
        raise BlockchainAPIError("Error trazando producto", response)
    return response.json()
