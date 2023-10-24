from django.urls import path
from authuser import views

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.handlelogin,name="handlelogin"),
    path('logout/',views.handlelogout,name="handlelogout"),
    path('profile/',views.handleprofile,name="handleprofile"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
]