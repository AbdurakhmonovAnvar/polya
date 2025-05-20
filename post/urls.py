from django.urls import path
from .views import CreatePolya,UpdatePolya,GetPolya, GetAllPolya, GetPolyaById

urlpatterns = [
    path('api/polya/create',CreatePolya.as_view(),name='create-polya'),
    path('api/polya/get-all',GetAllPolya.as_view(),name='get-all-polya'),
    path('api/polya/get-my-polyas',GetPolya.as_view(),name='get-my-polya'),
    path('api/polya/update/int:polya_id>',UpdatePolya.as_view(),name='update-polya'),
    path('api/polya/get-by-id-polya/<int:id>',GetPolyaById.as_view(),name='get-by-id-polya'),

# testcha bu
]