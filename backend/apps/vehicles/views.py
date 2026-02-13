from rest_framework.views import APIView
from rest_framework.response import Response
from .constants import (
    VEHICLE_TYPES,
    ENGINE_TYPES,
    DRIVE_TRAINS,
    TRANSMISSIONS
)
from .utils import filter_by_vehicle_type


class VehicleOptionsView(APIView):
    def get(self, request):
        vehicle_type = request.query_params.get("vehicle_type")

        return Response({
            "vehicleTypes": VEHICLE_TYPES,
            "engineTypes": ENGINE_TYPES,
            "driveTrains": filter_by_vehicle_type(DRIVE_TRAINS, vehicle_type),
            "transmissions": filter_by_vehicle_type(TRANSMISSIONS, vehicle_type),
        })
