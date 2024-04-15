from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=18, null=True, blank=True)
    country =  models.CharField(max_length=255, default = " ", null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile-picture/', default=" ")
    bio = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"
    
    #model to store followers and following
class Follower(models.Model):
    follower = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name = "follower")
    following = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name = "Following")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.user.username} is following {self.following.user.username}"
    
class PostLike(models.Model):
    artwork = models.ForeignKey("Artwork", on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A like on post {self.artwork.title} by {self.artist.user.username}"


class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to= 'artworks/')
    likes = models.ManyToManyField(Artist, related_name="liked_artworks", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title}"
    def artist_name(self):
        return f"{self.artist.user.first_name} {self.artist.user.last_name}"

class Comment(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist.user.username} {self.comment[:20]}"



class Transaction(models.Model):
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE, default="")
    purchase_date = models.DateTimeField(auto_now_add=True)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.cart.artist.user.username} - {self.purchase_date}"
    
class Cart(models.Model):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def cart_total(self):
        cart_total = 0
        for item in self.items.all():
            cart_total +=item.item_total
        return cart_total

    def __str__(self):
        return f"Cart for {self.artist.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    artwork=models.OneToOneField(Artwork, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def item_total(self):
        return self.artwork.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.artwork.title}"
    
class Query(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length = 255)
    message = models.TextField()

    def __str__(self):
        return self.email
