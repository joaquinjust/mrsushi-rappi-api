import functions_framework
import json
import uuid
from datetime import datetime

@functions_framework.http
def mrsushi_rappi(request):
    # Permitir CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    headers = {'Access-Control-Allow-Origin': '*'}

    # POST /orders - Crear pedido
    if request.method == 'POST' and '/orders' in request.path:
        data = request.get_json(silent=True) or {}
        order_id = str(uuid.uuid4())[:8].upper()
        order = {
            "order_id": f"ORD-{order_id}",
            "restaurante": "Mr Sushi",
            "cliente": data.get("cliente", "Cliente Rappi"),
            "items": data.get("items", []),
            "total": data.get("total", 0),
            "status": "RECEIVED",
            "origen": "RAPPI",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": "Pedido recibido por Rappi, enviado a Mr Sushi"
        }
        return (json.dumps(order), 200, headers)

    # PUT /orders/{id}/status - Actualizar estado
    if request.method == 'PUT' and '/status' in request.path:
        data = request.get_json(silent=True) or {}
        response = {
            "order_id": data.get("order_id", ""),
            "status": data.get("status", ""),
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "message": f"Estado actualizado en Rappi: {data.get('status', '')}"
        }
        return (json.dumps(response), 200, headers)

    # GET - Health check
    if request.method == 'GET':
        return (json.dumps({
            "service": "Mr Sushi - Rappi API",
            "status": "running",
            "cloud": "GCP",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200, headers)

    return (json.dumps({"error": "Endpoint no encontrado"}), 404, headers)
