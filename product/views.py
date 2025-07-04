from rest_framework import generics, permissions
from .models import Product, ProductUnit
from .serializers import ProductSerializer, ProductUnitSerializer
from .permissions import IsLaboratoryOwner
from laboratory.models import Laboratory
from django.shortcuts import get_object_or_404
from blockchain_client.services import register_event, trace_product
from blockchain_client.models import BlockchainEvent, Responsible, Geolocation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from batch.models import Series
from rest_framework.permissions import IsAuthenticated
import hashlib


def validate_required_fields(data, required_fields):
    for field in required_fields:
        if field not in data:
            return Response({"error": f"Campo '{field}' requerido."}, status=status.HTTP_400_BAD_REQUEST)
    return None

def get_user_laboratory(user):
    try:
        return user.laboratory, None
    except Laboratory.DoesNotExist:
        return None, Response({"error": "El usuario no tiene laboratorio asociado"}, status=400)



# POST /api/v1/products
class CreateProductView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        lab = Laboratory.objects.get(user=self.request.user)
        serializer.save(laboratory=lab)

# GET /api/v1/products
class ListProductView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        lab = Laboratory.objects.get(user=self.request.user)
        return lab.products.all()

# GET /api/v1/products/{id}
class RetrieveProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsLaboratoryOwner]

# PUT /api/v1/products/{id}
class UpdateProductView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsLaboratoryOwner]


class ProductUnitCreateView(generics.CreateAPIView):
    queryset = ProductUnit.objects.all()
    serializer_class = ProductUnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_unit = serializer.save()

        try:
            lab = Laboratory.objects.get(user=self.request.user)

            event = BlockchainEvent(
                labId=str(lab.id),
                eventType="manufacture",
                productSerial=product_unit.serial_number,
                batchId="SIN_BATCH",  # Si se vincula luego a un lote, actualizar en otro evento
                origin="Planta de producción",
                destination="Almacén central",
                currentLocation="Almacén central",
                responsible=Responsible(
                    name=self.request.user.username,
                    role="lab",
                    entity=lab.business_name,
                    documentId=lab.dni_representante
                ),
                notes=f"Unidad serial {product_unit.serial_number} fabricada.",
                digitalSignature="FIRMA_AUTO",  # Puedes reemplazar por hash real más adelante
                deviceInfo="Sistema Django",
                geolocation=Geolocation(
                    ip=self.get_client_ip(),
                    lat=10, 
                    lng=10
                )
            )

            register_event(event)

        except Exception as e:
            print(f"Error al registrar evento blockchain: {e}")


    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return self.request.META.get('REMOTE_ADDR', '127.0.0.1')


class ProductUnitListView(generics.ListAPIView):
    queryset = ProductUnit.objects.all()
    serializer_class = ProductUnitSerializer

class ProductUnitSeriesByProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id: int):
        # Ensure the product exists to return 404 if not
        get_object_or_404(Product, pk=product_id)
        units = ProductUnit.objects.filter(product_id=product_id)
        series = list(units.values_list("serial_number", flat=True))
        return Response({"series": series})


class TraceabilityBySeriesView(APIView):
    def get(self, request, serie):
        try:
            # Buscar la serie y el laboratorio asociado
            serie_obj = Series.objects.select_related('batch__laboratory').get(serie_code=serie)
            laboratorio = serie_obj.batch.laboratory

            # Llamar a la blockchain
            response = trace_product(str(laboratorio.id), serie)

            return Response(response.json(), status=response.status_code)

        except Series.DoesNotExist:
            return Response({"error": "Serie no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": "Fallo al consultar la blockchain", "detalle": str(e)}, status=500)
        


class RegisterBlockchainEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Validaciones mínimas
        error_response = validate_required_fields(data, ['productSerial', 'batchId', 'eventType', 'destination', 'deviceInfo', 'responsible', 'geolocation'])
        if error_response:
            return error_response

        # 1. Recuperar laboratorio
        lab, error_response = get_user_laboratory(user)
        if error_response:
            return error_response

        # 2. Trazar producto para obtener el último evento (origen)
        try:
            chain_response = trace_product(str(lab.id), data['productSerial'])
            chain_data = chain_response.json()
            events = chain_data.get('events', [])

            if not isinstance(events, list):
                return Response({"error": "El formato de respuesta de blockchain no es válido", "data": chain_data}, status=500)

            last_event = events[-1] if events else None
            origin = last_event['currentLocation'] if last_event else "Origen desconocido"
        except Exception as e:
            return Response({"error": f"Error al trazar producto: {str(e)}"}, status=500)

        # 3. Construir objeto BlockchainEvent
        responsible = Responsible(
            name=data['responsible']['name'],
            role=data['responsible']['role'],
            entity=lab.business_name,
            documentId=data['responsible']['documentId']
        )

        geolocation = Geolocation(
            ip=data['geolocation']['ip'],
            lat=data['geolocation'].get('lat', 0.0),
            lng=data['geolocation'].get('lng', 0.0)
        )

        signature_string = f"{lab.id}{data['eventType']}{data['productSerial']}{data['destination']}"
        digital_signature = hashlib.sha256(signature_string.encode()).hexdigest()

        event = BlockchainEvent(
            labId=str(lab.id),
            eventType=data['eventType'],
            productSerial=data['productSerial'],
            batchId=data['batchId'],
            origin=origin,
            destination=data['destination'],
            currentLocation=data['destination'],
            responsible=responsible,
            notes=data.get('notes', ''),
            digitalSignature=digital_signature,
            deviceInfo=data['deviceInfo'],
            geolocation=geolocation
        )

        try:
            result = register_event(event)
            return Response({"success": True, "blockchain_response": result}, status=200)
        except Exception as e:
            return Response({"error": f"Error registrando evento en blockchain: {str(e)}"}, status=500)



from anomaly_detection import predict as predict_trace

class AllAlertsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        alerts = []
        units = ProductUnit.objects.select_related('product__laboratory').all()

        for unit in units:
            lab = unit.product.laboratory
            try:
                response = trace_product(str(lab.id), unit.serial_number)
                if not response.ok:
                    print(f"Error HTTP al trazar {unit.serial_number}: {response.status_code}")
                    continue

                json_data = response.json()
                trace = json_data.get("trace")

                if not isinstance(trace, list):
                    print(f"'trace' no es una lista válida para {unit.serial_number}: {trace}")
                    continue

                if len(trace) < 2:
                    print(f"Trazabilidad muy corta (menos de 2 eventos) para {unit.serial_number}")
                    continue

                # Realizar predicción
                try:
                    probs = predict_trace(trace)
                except Exception as e:
                    print(f"Error durante la predicción de {unit.serial_number}: {str(e)}")
                    continue

                suspicious = [float(p) for p in probs if p >= 0.5]

                if suspicious:
                    alerts.append({
                        'product_serial': unit.serial_number,
                        'lab_id': lab.id,
                        'suspicious_scores': suspicious,
                    })

                print(f"{unit.serial_number} - Predicciones: {probs}")

            except Exception as e:
                print(f"Excepción inesperada para {unit.serial_number}: {str(e)}")
                continue

        return Response({'alerts': alerts})


class LabAlertsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lab_id: int):
        alerts = []
        units = ProductUnit.objects.filter(product__laboratory_id=lab_id).select_related('product__laboratory')

        for unit in units:
            try:
                response = trace_product(str(lab_id), unit.serial_number)
                if not response.ok:
                    print(f"Error HTTP para {unit.serial_number}: {response.status_code}")
                    continue

                json_data = response.json()
                trace = json_data.get("trace")

                if not isinstance(trace, list):
                    print(f"'trace' no es una lista válida para {unit.serial_number}: {trace}")
                    continue

                if len(trace) < 2:
                    print(f"Trazabilidad muy corta (menos de 2 eventos) para {unit.serial_number}")
                    continue

                try:
                    probs = predict_trace(trace)
                except Exception as e:
                    print(f"Error durante la predicción de {unit.serial_number}: {str(e)}")
                    continue

                suspicious = [float(p) for p in probs if p >= 0.5]

                if suspicious:
                    alerts.append({
                        'product_serial': unit.serial_number,
                        'lab_id': lab_id,
                        'suspicious_scores': suspicious,
                    })

                print(f"{unit.serial_number} - Predicciones: {probs}")

            except Exception as e:
                print(f"Excepción inesperada para {unit.serial_number}: {str(e)}")
                continue

        return Response({'alerts': alerts})
    

