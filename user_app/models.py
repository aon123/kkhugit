
from django.db import models
# 커스텀 유저 모델
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# class UserManager(BaseUserManager) :
#     def creaete_user(self, full_name, email, password=None):
#         if not email:
#             raise ValueError('이메일 주소를 반드시 입력하세요.')
#
#         user = self.model(
#             full_name=full_name,
#             email=self.normalize_email(email),
#             password=password,
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, full_name, email, password):
#         superuser = self.creaete_user(full_name, email, password)
#         superuser.is_admin = True
#         superuser.save(using=self._db)
#         return superuser



# Create your models here.

class Users(AbstractBaseUser):
    username = None
    last_login = None
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=45)
    email = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=45)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
# is_active, is_admin -> django user model 필수 필드
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

    # objects = UserManager()

 
    USERNAME_FIELD = 'email'  # 로그인 ID로 이메일 사용(Id 필드)
    REQUIRED_FIELDS = ['password'] # 필수 작성 필드


    class Meta:
        managed = True
        db_table = 'users'

