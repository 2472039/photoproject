from django.db import models
# AbstractUserをインポート
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # Userモデルを継承したカスタムユーザーモデル
    pass