from django.urls import path
from .views import CreatePolya, UpdatePolya, GetPolya, GetAllPolya, GetPolyaById, GetStreet, GetRegions, \
    GetPolyaByRegionAndStreet

urlpatterns = [
    path('api/polya/create', CreatePolya.as_view(), name='create-polya'),
    path('api/polya/get-streets-region/<str:region_name>', GetStreet.as_view(), name='get-steets'),
    path('api/polya/regions', GetRegions.as_view(), name='get-region'),
    path('api/polya/get-all', GetAllPolya.as_view(), name='get-all-polya'),
    path('api/polya/get-my-polyas', GetPolya.as_view(), name='get-my-polya'),
    path('api/polya/update/int:<polya_id>', UpdatePolya.as_view(), name='update-polya'),
    path('api/polya/get-by-id-polya/<int:id>', GetPolyaById.as_view(), name='get-by-id-polya'),
    path('api/polya/get-by-region-and-street-polya/<str:region_name>/<str:street_name>', GetPolyaById.as_view(),
         name='get-by-region-and-street-polya'),

]
# ass
# Bu test avtomat as
