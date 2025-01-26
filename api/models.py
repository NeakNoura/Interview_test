from django.db import models

class CategoryTB(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductTB(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/')
    price = models.FloatField()
    category = models.ForeignKey(CategoryTB, on_delete=models.CASCADE, related_name="products")
    features = models.JSONField(null=True, blank=True)
    def __str__(self):
        return self.name
