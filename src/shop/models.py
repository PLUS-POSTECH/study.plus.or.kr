import os

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model

from problem.models import ProblemList


User = get_user_model()


ShopImageStorage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'shop'))


class ShopItem(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    image = models.FileField(storage=ShopImageStorage)
    last_modified = models.DateTimeField(auto_now=True)
    price = models.IntegerField()
    chance = models.DecimalField(max_digits=4, decimal_places=2)
    hidden = models.BooleanField()

    class Meta:
        verbose_name = '상점 아이템'
        verbose_name_plural = '상점 아이템들'

    def __str__(self):
        return '%s' % self.title


class Shop(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    problem_list = models.OneToOneField(ProblemList, on_delete=models.PROTECT)
    shop_items = models.ManyToManyField(ShopItem)

    class Meta:
        verbose_name = '상점'
        verbose_name_plural = '상점들'

    def __str__(self):
        return '%s' % self.title


class ShopPurchaseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    shop = models.ForeignKey(Shop, on_delete=models.PROTECT)
    item = models.ForeignKey(ShopItem, on_delete=models.PROTECT)
    succeed = models.BooleanField()
    retrieved = models.BooleanField()
    purchase_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '상점 구매 로그'
        verbose_name_plural = '상점 구매 로그들'

    def __str__(self):
        return '[%s] %s: %s, %s' % \
            ("성공" if self.succeed else "실패", self.user, self.shop, self.item)
