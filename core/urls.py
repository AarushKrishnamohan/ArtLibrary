from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('contact', views.contact_page, name='contact'),
    path('about', views.about_page, name='about'),
    path('artwork-upload', views.artwork_upload, name='artwork-upload'),
    path('artwork_details/<int:pk>/', views.artwork_detail, name='artwork-details'),
    path('author-profile/<int:pk>/', views.author_profile, name='author-profile'),

    path('account-settings', views.account_settings, name="account-settings"),


    path('follow-user/', views.follow_user, name='follow-user'),
    path('unfollow-user/', views.unfollow_user, name='unfollow_user'),
    path('add-comment/', views.add_comment, name="add-comment"),


    path('like-post/', views.likePost, name='like-post'),

    path('cart/', views.cart, name='cart'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('delete-cart-item/<int:item_id>/', views.delete_cart_item, name='delete-cart-item'),

    path('checkout/', views.checkout, name='checkout'),
    path('checkout/checkoutconfirm/', views.checkoutconfirm, name="checkout-confirm")


]
