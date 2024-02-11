
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from demo.views import UserViewset


router = DefaultRouter()
router.register("users", UserViewset, basename="Users")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]


urlpatterns += router.urls