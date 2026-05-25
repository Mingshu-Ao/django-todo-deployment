from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    # 建立外键关联，级联删除，设置默认值为空
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)