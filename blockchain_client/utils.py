def validar_event_type(event_type: str):
    valid_types = {"manufacture", "shipment", "reception", "sale", "return", "query"}
    if event_type not in valid_types:
        raise ValueError(f"Tipo de evento no permitido: {event_type}")

