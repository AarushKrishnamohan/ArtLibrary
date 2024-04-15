from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .models import Artwork, Artist, Follower, Query, Comment, PostLike, Transaction, Cart, CartItem
from django.contrib.auth.models import User

# Create your views here.
def artist_of_the_month():
    artists = Artist.objects.all()
    likes_list = []
    for artist in artists:
        likes_mapping = {}
        likes = 0
        artworks = Artwork.objects.filter(artist=artist)
        for artwork in artworks:
            likes += artwork.likes.all().count()
        likes_mapping = {'artist': artist, 'likes': likes}
        likes_list.append(likes_mapping)

    max = likes_list[0]
    for likes in likes_list:
        if likes['likes'] > max['likes']:
            max = likes
    return max

def display_cart_count(request):
    artist = Artist.objects.get(user=request.user)
    try:
        cart = Cart.objects.get(artist=artist)
        return cart.items.all().count()
    except Cart.DoesNotExist:
        return 0

def check_relation(request, pk):
    logged_in_artist = Artist.objects.get(user=request.user)
    artist = Artist.object.get(pk=pk)
    conn = False

    for follower in artist.following.all():
        if logged_in_artist == follower.follower:
            conn = True
        return conn
def home(request):
    artworks = Artwork.objects.all()
    cart_count = display_cart_count(request)
    best_artist = artist_of_the_month()
    context = {
        'artworks': artworks,
        'count': cart_count,
        'best_artist': best_artist['artist']
    }
    return render(request, 'core/home.html', context)

def feed(request):
    if request.user.is_authenticated:
        artist = Artist.objects.get(user=request.user)
        artworks = Artwork.objects.all().exclude(artist=artist)
    else:
        return redirect('login')
    cart_count = display_cart_count(request)
    context={
        'artworks': artworks,
        'artist': artist,
        'count': cart_count
    }
    return render(request, 'core/feed.html', context)

def contact_page(request):
    cart_count = display_cart_count(request)
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        new_query = Query.objects.create(name=name, email=email, message=message)
        new_query.save()

        return JsonResponse({"type": "success", "message": "Your query has been submitted, we will get in touch with you soon"})
    context={
        'count': cart_count
    }
    return render(request, 'core/contact.html', context)


def add_comment(request):
    if request.method == 'POST':
        user = request.user
        comment = request.POST.get('comment')
        artwork_id = request.POST.get('artwork_id')

        artwork = Artwork.objects.get(pk=artwork_id)

        artist = Artist.objects.get(user=user)
        new_comment = Comment.objects.create(artist=artist, comment=comment)
        new_comment.save()

        if new_comment:
            return JsonResponse({'type': 'success', 'message': 'Your comment has been posted'})
        else:
            return JsonResponse({'type': 'error', 'message': 'Something has happeend while posting your comment'})


def about_page(request):
    cart_count = display_cart_count(request)
    context={
        'count': cart_count
    }
    return render(request, 'core/about.html', context)

def artwork_upload(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES['image']


        #artist object
        artist, created = Artist.objects.get_or_create(user=user)

        new_artwork = Artwork.objects.create(title=title, description=description, artist=artist, price=price, image=image)
        new_artwork.save()
        if new_artwork:
            return redirect('home')
    return render(request, 'core/artwork_upload.html')

def artwork_detail(request, pk):

    artwork = Artwork.objects.get(pk=pk)
    context = {'artwork': artwork}
    return render(request, 'core/artwork_details.html', context)

def author_profile(request, pk):
    conn = check_relation(request, pk)
    logged_in_artist = Artist.objects.get(user=request.user)
    artist = Artist.objects.get(pk=pk)
    followers_count = Follower.objects.filter(following=artist).count()
    following_count = Follower.objects.filter(follower=artist).count()


    artworks = Artwork.objects.filter(artist=artist)
    context={
        'artist': artist,
        'conn': conn,
        'logged_in_artist': logged_in_artist,
        'artworks': artworks,
        'followers_count': followers_count,
        "following_count": following_count

    }
    return render(request, 'core/author_profile.html', context)

def account_settings(request):
    artist = Artist.objects.get(user=request.user)
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        country = request.POST.get('country')
        bio = request.POST.get('bio')

        profile_picture = request.FILES.get('image') if 'image' in request.FILES else artist.profile_picture

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()

        artist.user = user
        artist.age = age
        artist.country = country
        artist.bio = bio
        artist.profile_picture = profile_picture

        artist.save()
        return JsonResponse({"type": "success", "message": "Your Details have been  Saved"})

    context={'artist': artist}
    return render(request, 'core/account_settings.html', context)

def follow_user(request):
    if request.method =='POST':
        followingId = request.POST.get('following_id')

        follower = Artist.objects.get(user=request.user)
        following = Artist.objects.get(pk=followingId)

        new_relation = Follower.objects.create(follower=follower, following=following)
        new_relation.save()


        if new_relation:
            return JsonResponse({'type': 'success', 'message': f'You are following {following.user.username}'})
        else:
            return JsonResponse({'type': 'error', 'message': "something went wrong"})
        
def unfollow_user(request):
    if request.method =='POST':
        followingId = request.POST.get('following_id')

        follower = Artist.objects.get(user=request.user)
        following = Artist.objects.get(pk=followingId)

        relation = Follower.objects.get(follower=follower, following=following)
        relation.delete()

        return JsonResponse({'type': 'success', 'message': f'You have unfollowed {following.user.username}'})
    

def likePost(request):
    artist = Artist.objects.get(user=request.user)

    if request.method == 'POST':
        artwork_id = request.POST.get('artwork_id')

        artwork = Artwork.objects.get(id=artwork_id)
        if artist in artwork.likes.all():
            artwork.likes.remove(artist)
            return JsonResponse({'type': 'success', 'message': 'Post Unliked'})
        else:
            artwork.likes.add(artist)
            return JsonResponse({'type': 'success', 'message': 'post liked'})


def cart(request):
    context = {}
    shipping_fee = 15
    artist = Artist.objects.get(user=request.user)
    cart_count = display_cart_count(request)
    try:
        cart = Cart.objects.get(artist=artist)
        cart_items = CartItem.objects.filter(cart=cart)
        subtotal = cart.cart_total + shipping_fee
        context = {'cart': cart, 'cart_items': cart_items, 'count': cart_count, 'subtotal': subtotal, 'shipping_fee': shipping_fee}
    except:
        pass
    return render(request, 'core/cart.html', context)


def add_to_cart(request):
    if request.method == 'POST':
        artwork_id = request.POST.get('artwork_id')
        artist = Artist.objects.get(user=request.user)

        artwork = Artwork.objects.get(id=artwork_id)
        cart, created = Cart.objects.get_or_create(artist=artist)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, artwork=artwork)

        if not created:
            cart_item.quantity +=1
            cart_item.save()

        return redirect('cart')

def delete_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')

def checkout(request):
    shipping_fee = 15
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')

        cart = Cart.objects.get(id=cart_id)
        cart_total = cart.cart_total + shipping_fee
        new_transactions = Transaction.objects.create(cart=cart, price_paid=cart_total)
        new_transactions.save()

        if new_transactions:
            return redirect('checkout-confirm')
        else:
            return JsonResponse({'type': 'error', 'message': 'something went wrong'})



def checkoutconfirm(request):
    return render(request, 'core/checkoutconfirm.html')