from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

# Create your models here.
class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    create_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(auto_now=True)

class User(BaseModel):
    username = models.CharField(blank=False, max_length=50, db_index=True, unique=True)
    email = models.EmailField(max_length=255, verbose_name='email address', unique=True, blank=False, null=False)
    address = models.CharField(null=False, blank=False, max_length=255)

class Stock(BaseModel):
    title = models.CharField(blank=False, max_length=100, db_index=True, unique=True)
    description = models.CharField(null=False, blank=False, max_length=255)

class Product(BaseModel):
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    title = models.CharField(blank=False, max_length=100, db_index=True, unique=True)
    description = models.CharField(null=False, blank=False, max_length=255)
    unit_price = models.FloatField(default=None, null=True, blank=False)
    quantity = models.IntegerField(default=3600, null=False, blank=False)
    stocks = models.ForeignKey(Stock, null=False, blank=False, on_delete=models.CASCADE)

class SaleOrder(BaseModel):
    total_price = models.FloatField(default=None, null=True, blank=False)
    products = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    users = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
