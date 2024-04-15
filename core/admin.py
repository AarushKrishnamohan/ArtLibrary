from django.contrib import admin
from .models import Artist, Artwork, Transaction, Follower, Query, Comment, PostLike, Cart, CartItem
# Register your models here.

admin.site.register((Artist, Artwork, Transaction, Follower, Query, Comment, PostLike, Cart, CartItem))
