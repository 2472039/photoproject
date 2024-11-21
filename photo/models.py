from django.db import models
# accountsアプリのmodelsモジュールからCustomUserをインポート
from accounts.models import CustomUser

# Create your models here.
class Category(models.Model):
    # 投稿する写真のカテゴリを管理するモデル
    # カテゴリ名のフィールド
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20
    )
    
    def __str__(self):
        # オブジェクトを文字列に変換して返す
        return self.title
    
class PhotoPost(models.Model):
    # 投稿されたデータを管理するモデル
    '''
    CustomUserモデル(のuser_id)とPhotoPostモデルを1対多の関係で結びつける
    CustomUserが親でPhotoPostが子の関係となる
    '''
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        # ユーザーを削除する場合はそのユーザーの投稿データもすべて削除する
        on_delete=models.CASCADE
    )
    '''
    Categoryモデル(のtitle)とPhotoPostモデルを1対多の関係で結びつける
    CustomUserが親でPhotoPostが子の関係となる
    '''
    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        # カテゴリに関連付けられた投稿データが存在する場合はそのカテゴリを削除できないようにする
        on_delete=models.PROTECT
    )
    
    # タイトル用のフィールド
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
    )
    # コメント用のフィールド
    comment = models.TextField(
        verbose_name='コメント'
    )
    # イメージのフィールド1
    image1 = models.ImageField(
        verbose_name='イメージ1',
        upload_to= 'photos'         # MEDIA_ROOT以下のphotosにファイルを保存
    )
    # イメージのフィールド2
    image2 = models.ImageField(
        verbose_name= 'イメージ2',
        upload_to= 'photos',
        blank = True,        # フィールドの設定は必須でない
        null = True,         # データベースにnullが保存されることを許容
    )
    # 投稿日時のフィールド
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )
    
    def __str__(self):
        # オブジェクトを文字列に変換して返す
        return self.title