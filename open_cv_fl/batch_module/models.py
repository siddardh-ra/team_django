from django.db import models
from django.contrib.auth.models import User
from datetime import  datetime
from django.utils import timezone
import uuid


class Batch(models.Model):
    name = models.CharField(max_length = 255,unique = True)
    project = models.CharField(max_length = 255)
    location_code = models.CharField(max_length = 255)
    short_description = models.CharField(max_length = 255)
    description = models.TextField(default='')
    total_images = models.IntegerField(default= 0)
    failed_images = models.IntegerField(default= 0)
    batch_status = models.IntegerField(default= 0)
    profile = models.CharField(max_length = 255)
    csv_file_url = models.URLField()
    config = models.TextField(default='{}')
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(default = timezone.now)
    created_by = models.ForeignKey(User,on_delete = models.CASCADE)
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'batches'

    def __str__(self):
        return self.project+"_"+self.name


class ImageBank(models.Model):
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    file_name=models.CharField(max_length=255,default="",blank=True,null=True)
    URL=models.CharField(max_length=255,default="",blank=True,null=True)
    no_of_samples=models.IntegerField(default=0)
    sample_details=models.TextField(default={},blank=True,null=True)
    request_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status=models.IntegerField(default=0)
    config=models.TextField(default={})

    def __str__(self):
        return str(self.file_name)+"_"+str(self.batch)
