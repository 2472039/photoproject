from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import PhotoPostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import PhotoPost
from django.views.generic import DetailView
from django.views.generic import DeleteView

# Create your views here.
class IndexView(ListView):
    template_name = 'index.html'
    queryset = PhotoPost.objects.order_by('-posted_at')
    paginate_by = 9
    
# デコレーターにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    '''
    写真投稿のビュー
    PhotopostFormで鄭げされているモデルとフィールドと連携して投稿データをデータベースに登録する
    
    Attributes:
        form_class: モデルとフィールドが登録されたフォームクラス
        template_name: レンダリングするテンプレート
        success_url: データベースへの登録完了後のリダイレクト先
    '''
    # forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class = PhotoPostForm
    template_name = "post_photo.html"
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('photo:post_done')
    
    def form_valid(self, form):
        '''
        CreateViewクラスのform_valid()をオーバーライド
        
        フォームのバリデーションを通過したときに呼ばれるフォームデータの登録をここで行う
        
        parameters:
            form(django.forms.Form):
            form_classに格納されているPhotoPotFormオブジェクト
        Return:
            HttpResponseRedirectオブジェクト:
                スーパークラスのform_valid()の戻り値を返すことで、success_urlで設定されているURLにリダイレクトさせる
        '''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    template_name = 'post_success.html'
    
class CategoryView(ListView):
    template_name = 'index.html'
    paginate_by = 9
    
    def get_queryset(self):
        '''
        クエリを実行する
        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する
        
        Returns:
            クエリによって取得されたレコード
        '''
        # self.kwargsでキーワードの辞書を取得し、categoryキーの値(Categoryテーブルのid)を取得
        category_id = self.kwargs['category']
        # filter(フィールド名=id)で絞り込む
        categories = PhotoPost.objects.filter(category=category_id).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return categories
    
class UserView(ListView):
    template_name = 'index.html'
    paginate_by = 9
    
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = PhotoPost.objects.filter(user=user_id).order_by('-posted_at')
        return user_list

class DetailView(DetailView):
    template_name = 'detail.html'
    model = PhotoPost
    
class MypageView(ListView):
    template_name = 'mypage.html'
    paginate_by = 9
    
    def get_queryset(self):
        # 現在ログインしているユーザー名はHttpRequest.userに格納されている
        # filter(userフィールド=userオブジェクト)で絞り込む
        queryset = PhotoPost.objects.filter(user=self.request.user).order_by('-posted_at')
        return queryset
    
class PhotoDeleteView(DeleteView):
    # 操作の対象はPhotoPostモデル
    model = PhotoPost
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('photo:mypage')
    
    def delete(self, request, *args, **kwargs):
        '''
        parameters:
            self: PhotoDeleteViewオブジェクト
            request: WSGIRequest(HttpRequest)オブジェクト
            args: 引数として渡される辞書(dict)
            kwargs: キーワード付きの辞書(dict)
                {'pk': 21}のようにレコードのidが渡される
        '''
        # スーパークラスのdelete()を実行
        return super().delete(request, *args, **kwargs)