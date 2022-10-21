from django.db import models

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=255)
    size = models.CharField(max_length=7, null=True)
    color = models.CharField(max_length=20, null=True)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='shop/images', default='')
    himage = models.ImageField(upload_to='shop/images', default='', blank=True)

    def __str__(self):
        return self.product_name

