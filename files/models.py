
from django.conf import settings
from dropbox import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import boto3

User = get_user_model()

class Files(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    size = models.IntegerField()
    favorites = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)
    shared_with = models.ManyToManyField(User, related_name='shared_files')
    user_id = models.ForeignKey(User, to_field = 'id', on_delete=models.CASCADE, db_column="user_id_id")
    memo = models.TextField(null=True)
    folder_id = models.CharField(max_length=255, default="Home")
    version = models.IntegerField(default=1)
    removed = models.BooleanField(default=False)
    s3key = models.CharField(max_length=255, null=True)
    clicked = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0) # 조회 횟수를 기록하는 어트리뷰트

    def watched(self, *args, **kwargs):
        # Mark the file as False from removed
        self.clicked +=1
        self.save(update_fields=['clicked'])
   

    def increase_view_count(self):
        self.view_count += 1
        self.save()

    def removing(self, *args, **kwargs):
        # Mark the file as removed instead of actually deleting it
        self.removed = True
        self.save()

    def recover(self, *args, **kwargs):
        # Mark the file as False from removed
        self.removed = False
        self.save(update_fields=['removed'])


    def completely_delete(self,  *args, **kwargs):
        # Delete the file from the S3 bucket
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        s3_bucket_name = 'suhron'
        s3_key = self.s3key.split('/')[-1]
        s3_client.delete_object(Bucket=s3_bucket_name, Key=s3_key)

        # Delete the file from the database
        self.delete()

    class Meta:
        managed = True
        db_table = "files"


class Folders(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, to_field = 'id', on_delete=models.CASCADE, db_column="user_id_id")

    class Meta:
        managed = True
        db_table = "folders"


