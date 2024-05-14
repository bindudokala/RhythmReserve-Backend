from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("password_reset_request/", views.password_reset_request,
         name="password_reset_request"),
    path("verify_reset_code/", views.verify_reset_code, name="verify_reset_code"),
    path("password_reset_post/", views.reset_password_post,
         name="reset_password_post"),

    path('google_signin/', views.google_signin, name='google_signin'),
    path('google_signup/', views.google_signup, name='google_signup'),
    path('google_email/', views.google_email, name='google_email'),
    path("get_user_data/", views.get_user_data, name='get_user_data'),
    path("get_user_id/", views.get_user_id, name="get_user_id")

]

