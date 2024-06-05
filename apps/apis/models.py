from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserAccount(BaseModel):
    username = models.CharField(blank=False, max_length=50, db_index=True, unique=True)
    email = models.EmailField(max_length=255, verbose_name='email address', unique=True, blank=False, null=False)
    address = models.CharField(null=False, blank=False, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def details_context(self):
        return {
            'id':self.pk,
            'username':self.username,
            'email':self.email,
            'address':self.address,
            'create_at':self.create_at,
            'update_at':self.updated_at,
        }

class Product(BaseModel):
    image = models.ImageField(upload_to='product_images/', height_field=None, width_field=None, max_length=100)
    title = models.CharField(blank=False, max_length=100, db_index=True, unique=True)
    description = models.CharField(null=False, blank=False, max_length=255)
    unit_price = models.FloatField(default=None, null=True, blank=False)
    quantity = models.IntegerField(default=3600, null=False, blank=False)

class SaleOrder(BaseModel):
    total_price = models.FloatField(default=None, null=True, blank=False)
    products = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    users = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
