from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm

urlpatterns = [
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path(
        "product-detail/<int:pk>", views.ProductDetails.as_view(), name="product-detail"
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.AddressView.as_view(), name="address"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="showcart"),
    path("checkout/", views.Checkout.as_view(), name="checkout"),
    path("pluscart/", views.plus_cart),
    path("minuscart/", views.minus_cart),
    path("removecart/", views.remove_cart),
    # //login Authentication
    path(
        "registration",
        views.CustomerRegistrationView.as_view(),
        name="customerregistration",
    ),
    path(
        "accounts/login/",
        auth_view.LoginView.as_view(
            template_name="app/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    path(
        "password-reset/",
        auth_view.PasswordResetView.as_view(
            template_name="app/password_reset.html", form_class=MyPasswordResetForm
        ),
        name="password_reset",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
