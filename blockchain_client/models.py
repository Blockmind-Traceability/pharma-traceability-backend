from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class Responsible:
    name: str
    role: str
    entity: str
    documentId: str

@dataclass
class Geolocation:
    ip: str
    lat: float
    lng: float

@dataclass
class BlockchainEvent:
    labId: str
    eventType: str
    productSerial: str
    batchId: str
    origin: str
    destination: str
    currentLocation: str
    responsible: Responsible
    notes: str
    digitalSignature: str
    deviceInfo: str
    geolocation: Geolocation

@dataclass
class GenesisBlock:
    labId: str
    business_name: str
    ruc: str
    representante_legal: str
    dni_representante: str
