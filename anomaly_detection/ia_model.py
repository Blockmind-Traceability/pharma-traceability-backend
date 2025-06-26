import numpy as np
from datetime import datetime
from keras.models import load_model
import os

# Mapping of event types used during training
EVENT_TYPE_MAP = {
    "manufacture": 0,
    "shipment": 1,
    "reception": 2,
    "sale": 3,
    "return": 4,
    "query": 5,
}


def normalize_lat(lat: float) -> float:
    return (lat + 90) / 180


def normalize_lng(lng: float) -> float:
    return (lng + 180) / 360


def normalize_timestamp_delta(delta: float, max_seconds: int = 300) -> float:
    return min(delta / max_seconds, 1.0)


def normalize_event_type(event_type: str) -> float:
    return EVENT_TYPE_MAP.get(event_type, 0) / 5


def preprocess_trace(trace):
    """Convert a list of event dicts into feature vectors."""
    vectors = []
    for i in range(1, len(trace)):
        prev = trace[i - 1]
        curr = trace[i]
        t1 = datetime.fromisoformat(prev["eventDate"].replace("Z", "+00:00"))
        t2 = datetime.fromisoformat(curr["eventDate"].replace("Z", "+00:00"))
        timestamp_delta = (t2 - t1).total_seconds()

        vector = [
            normalize_lat(curr["geolocation"]["lat"]),
            normalize_lng(curr["geolocation"]["lng"]),
            normalize_timestamp_delta(timestamp_delta),
            1 if curr.get("deviceInfo") == prev.get("deviceInfo") else 0,
            1 if curr["responsible"].get("documentId") == prev["responsible"].get("documentId") else 0,
            1 if curr.get("digitalSignature") == prev.get("digitalSignature") else 0,
            normalize_event_type(curr["eventType"]),
        ]
        vectors.append(vector)
    return np.array(vectors, dtype=np.float32)


_model = None


def get_model(model_path: str = "modelo_ia.keras"):
    """Load the Keras model lazily and cache it."""

    global _model
    if _model is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        _model = load_model(model_path)

    return _model


def predict(trace):
    X = preprocess_trace(trace)
    if X.size == 0:
        return np.array([])
    model = get_model()
    preds = model.predict(X)
    return preds.flatten()


