from django.db import models


class ProductModel(models.Model):
    title = models.CharField(max_length=50)
    composition = models.TextField(null=False, blank=False)
    price = models.FloatField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(to='CategoryModel', to_field='id', on_delete=models.CASCADE,
                                 related_name='product_category')
    image = models.ImageField(upload_to='media/products')
    discount = models.BooleanField()
    oldprice = models.FloatField(null=True, blank=True)
    new = models.BooleanField(default=False)
    hit = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'

    def __str__(self):
        return self.title


class CategoryModel(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
