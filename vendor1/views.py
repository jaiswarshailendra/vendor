from django.shortcuts import render
from .serial import Vendor_Serializer,Purchase_Serializer,Performance_Serializer
from .models import Vendor_Model,Purchase_Order_Model,Historical_Performance_Model
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

# Create your views here.

class Vendor_View(ModelViewSet):#CRUD operation on vendor Model
    queryset = Vendor_Model.objects.all()
    serializer_class=Vendor_Serializer
    
class Purchase_View(ModelViewSet): # CRUD operation on Purchase Model
    queryset = Purchase_Order_Model.objects.all()
    serializer_class=Purchase_Serializer

class Perf_View(APIView): 

    def get(self,request,id):
        completed_count=Purchase_Order_Model.objects.filter(vendor=id,status="completed").count() # get count of PO's where status is completed

        Purchase_count=Purchase_Order_Model.objects.filter(vendor=id).count() # get total number of Po's

        Vendor_Detail=Vendor_Model.objects.get(vendor_code=id) # get vendor model as per vendor_id

        Qual_Rat_Avg = sum(int(qr) for qr in Purchase_Order_Model.objects.filter(vendor=id,
                                 status="completed", quality_rating__isnull=False).values_list("quality_rating", flat=True))#Get total of quality rating given to specfic vendor
        
        Po_completed=Purchase_Order_Model.objects.filter(vendor=id, status="completed").values_list("po_number").count()#fetch all Po's number where status is completed and add them

        Po_Issue=Purchase_Order_Model.objects.filter(vendor=id).values_list("issue_date") # fetch all issue date as per vendor id 

        Po_acknowledgment=Purchase_Order_Model.objects.filter(vendor=id).values_list("acknowledgment_date") # fetch all accknowledgement date as per vendor id 

        date_month_year_Issue = [(Iss_dt[0].day+ Iss_dt[0].month+ Iss_dt[0].year) for Iss_dt,Ack_dt  in zip(Po_Issue,Po_acknowledgment) if Ack_dt[0]!=None ] 
        date_month_year_Acknowledgment = [(dt[0].day+ dt[0].month+ dt[0].year) for dt in Po_acknowledgment if dt[0]!=None]

        Acknowledge_Issue=sum((i-j) for i,j in zip(date_month_year_Acknowledgment,date_month_year_Issue))/Purchase_count # finds the difference between acknowledgement and 
                                                                                                                        # issue date then add them and divide them with 
                                                                                                                        # total number of po's
        Vendor_Detail.on_time_delivery_rate=(completed_count/Purchase_count) 
        Vendor_Detail.quality_rating_avg=(Qual_Rat_Avg/completed_count)
        Vendor_Detail.average_response_time=Acknowledge_Issue
        Vendor_Detail.fulfillment_rate=(Po_completed/Purchase_count)
        Vendor_Detail.save() 

        query=Historical_Performance_Model.objects.filter(vendor=id)
        serializer=Performance_Serializer(query,many=True)

        if query:   #update Performane History if it is in database as per performance id
            Performance=Historical_Performance_Model.objects.filter(vendor=id)
            Performance.update(date=timezone.now(),
                on_time_delivery_rate=Vendor_Detail.on_time_delivery_rate,
                quality_rating_avg=Vendor_Detail.quality_rating_avg,
                average_response_time=Vendor_Detail.average_response_time,
                fulfillment_rate=Vendor_Detail.fulfillment_rate)
            
        else:         # create Performance History if it is not in database as per vendor id
            Performance=Historical_Performance_Model(
                vendor=Vendor_Detail,
                date=timezone.now(),
                on_time_delivery_rate=Vendor_Detail.on_time_delivery_rate,
                quality_rating_avg=Vendor_Detail.quality_rating_avg,
                average_response_time=Vendor_Detail.average_response_time,
                fulfillment_rate=Vendor_Detail.fulfillment_rate
            )
            Performance.save()
        
        return Response(serializer.data,status=status.HTTP_200_OK)
        
