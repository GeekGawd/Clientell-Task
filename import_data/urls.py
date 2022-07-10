from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.AccessTokenView.as_view()),
    path('import/', views.ImportSalesForceData.as_view()),
    path('opportunity/', views.OpportunityGetAPI.as_view()),
    path('account/', views.AccountGetAPI.as_view()),
    path('user/', views.UserGetAPI.as_view()),
]
