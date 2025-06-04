from django.urls import path,include
from . import views

urlpatterns = [
    path('categories', views.GetCategories.as_view()),
    path('styles', views.GetStyles.as_view()),
    path('style/<slug>', views.GetStyle.as_view()),
    path('category/all', views.GetAllProducts.as_view()),
    # path('category/<slug>', views.GetCategory.as_view()),
    path('product/<slug>', views.GetProduct.as_view()),
    path('popular', views.GetPopularProducts.as_view()),
    path('search', views.ProductSearchView.as_view()),
]
