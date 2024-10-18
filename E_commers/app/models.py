from django.db import models
from  django.utils import timezone
from ckeditor.fields import RichTextField
from  django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name



class Brand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Filter_price(models.Model):
    FILTER_PRICE=(
        ('1000 TO 10000','1000 TO 10000'),
        ('10000 TO 20000','10000 TO 20000'),
        ('20000 TO 30000','20000 TO 30000'),
        ('30000  TO 40000','30000  TO 40000'),
        ('40000  TO 50000', '40000  TO 50000')

    )
    price = models.CharField(choices=FILTER_PRICE,max_length=60)
    def __str__(self):
        return self.price

class Product(models.Model):
    CONDITION = (('New','New'),('Old','Old'))
    STOCK = (('In Stock','In Stock'),('Out OF Stock','Out OF Stock'))
    STATUS = (('Publish','Publish'),('Draft','Draft'))


    unique_id = models.CharField(unique=True,max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="product_images/img")
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION,max_length=100)
    information = RichTextField(null=True)
    description= RichTextField(null=True)
    stock = models.CharField(choices=STOCK,max_length=200)
    status = models.CharField(choices=STATUS, max_length=200)
    created_date = models.DateTimeField( default=timezone.now)

    categories = models.ForeignKey(Categories,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    color =models.ForeignKey(Color,on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_price,on_delete=models.CASCADE)


    def save(self,*args,**kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id= self.created_date.strftime('75%Y%m%d23')+str(self.id)
        return super().save(*args,**kwargs)
    def __str__(self):
        return self.name


class Images(models.Model):
    image = models.ImageField(upload_to='Product_image/img')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Contact_us(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email




class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # Allow null for guest checkout
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.email}"









class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Product_Images/order_Img")
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)
    def __str__(self):
        return self.order.user.username


