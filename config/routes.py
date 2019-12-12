from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from core import views as core_views
from pesanan import views as pesanan_views


router = routers.DefaultRouter(trailing_slash=True)
router.register(r'users', core_views.UserViewset, base_name='user')
router.register(r'makanan', pesanan_views.MakananViewset, base_name='makanan')
router.register(r'minuman', pesanan_views.MinumanViewset, base_name='minuman')
router.register(r'pesanan', pesanan_views.PesananViewset, base_name='pesanan')
router.register(r'daftar-pesanan', pesanan_views.DaftarPesananViewset,
                base_name='daftar-pesanan')

urlpatterns = router.urls

urlpatterns += (
    path(r'auth/', obtain_jwt_token, name='auth'),
)
