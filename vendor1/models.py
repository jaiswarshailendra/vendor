from django.db import models

# Create your models here.
class Vendor_Model(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    contact_details=models.TextField(null=False)
    address=models.TextField(null=False)
    vendor_code=models.CharField(max_length=250,null=False,unique=True,primary_key=True)
    on_time_delivery_rate=models.FloatField(null=True)
    quality_rating_avg=models.FloatField(null=True)
    average_response_time=models.FloatField(null=True)
    fulfillment_rate=models.FloatField(null=True)

    def __str__(self):
        return self.vendor_code
    
choice=(
    ("pending","pending"),
    ("completed","completed"),
    ("canceled","canceled"),
    ("delay","delay")
)

rating=(
    ("0","0"),
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5")
)

class Purchase_Order_Model(models.Model):
    po_number=models.CharField(max_length=250,null=False,unique=True,primary_key=True)
    vendor=models.ForeignKey(Vendor_Model,on_delete=models.CASCADE)
    order_date=models.DateTimeField(null=False)
    delivery_date=models.DateTimeField(null=False)
    items=models.JSONField()
    quantity=models.IntegerField(null=False)
    status=models.CharField(max_length=20,choices=choice)
    quality_rating=models.CharField(max_length=10,choices=rating,default=0)
    issue_date=models.DateTimeField()
    acknowledgment_date=models.DateTimeField(null=True)
    
class Historical_Performance_Model(models.Model):
    vendor=models.ForeignKey(Vendor_Model,on_delete=models.CASCADE)
    date=models.DateTimeField()
    on_time_delivery_rate=models.FloatField()
    quality_rating_avg=models.FloatField()
    average_response_time=models.FloatField()
    fulfillment_rate=models.FloatField()