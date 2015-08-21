from django.conf.urls import include, url
from django.contrib import admin

from records.urls import router as records_router

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(records_router.urls)),
]
