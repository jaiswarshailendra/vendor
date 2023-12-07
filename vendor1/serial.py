from rest_framework.serializers import ModelSerializer
from .models import Vendor_Model,Purchase_Order_Model,Historical_Performance_Model

class Vendor_Serializer(ModelSerializer):
    class Meta:
        model=Vendor_Model
        fields="__all__"

class Purchase_Serializer(ModelSerializer):
    class Meta:
        model=Purchase_Order_Model
        fields="__all__"

class Performance_Serializer(ModelSerializer):
    class Meta:
        model=Historical_Performance_Model
        fields="__all__"