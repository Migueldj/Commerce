from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.base import Model
from django.db.models.deletion import RESTRICT
from django.db.models.fields import IntegerField, URLField
from django.db.utils import Error
from django.forms.fields import TypedMultipleChoiceField
from django.forms.models import ModelChoiceField
from django.forms.widgets import Input, Select, TextInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Bid, Commentary, Listing, User, Category
from django.forms import ModelForm,Textarea, NumberInput, URLInput # lo importé para hacer un form a partir de un model definido
from django.contrib.auth.decorators import login_required # lo importé para que solo usuarios registrados accesen a cierta vista

def index(request):
    listings = Listing.objects.filter(active=True) # aqui puedo agregar bool y exclude solo para los activos o filter
    onIndex = True
    return render(request, "auctions/index.html", {
        "listings": listings,
        "onIndex": onIndex,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description', 'category', 'bid', 'imageURL'] #Con esto selecciono los campos que quiero que aparezcan y el orden
        widgets = { #Esto lo hice para poder cambiar el tipo de widget y agregar atributos html
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'rows':4,}),
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title',}),
            'bid': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Initial Bid',}),
            'imageURL': URLInput(attrs={'class': 'form-control', 'placeholder': 'URL of Image',}),
            'category': Select(attrs={'class': 'form-control',})
        }
        labels={ #Esto cambia el label con que aparece el input 
            'bid': 'Initial Bid',
            'imageURL': 'Image'
        }


@login_required(login_url = 'login') # esto funciona como un reverse, utiliza un name de los urls definidos para redirigir a los usuarios que no han iniciado sesión
def create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            newListing = form.save(commit=False)  # commit=False Evita que se envíe directo el form ya que falta llenar los datos de usuario
            newListing.user = request.user #Con esto agrego al usuario que hizo la publicación a la DB 
            newListing.save()
            #newListing.save_m2m() # Este lo usaria si agregara datos del tipo ManyToMany
            listing=Listing.objects.get(pk=newListing.id) # lo usaré para direccionar al usuario al listing creado 
            '''
            #Esto me regresaría a la pagina de create para que el usuario pueda hacer otro listing
            return render(request, "auctions/create.html",{
                "form":ListingForm()
            })
            '''
            return HttpResponseRedirect(reverse("listing", kwargs={'category_name':listing.category,'listing_id':listing.id}))
        else:
            return render(request, "auctions/create.html",{
                "form":form
            })
    return render(request, "auctions/create.html", {
        "form":ListingForm()
    })

@login_required(login_url = 'login')
def watchlist(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    if user.userWatchlist.filter(pk=listing.id).exists():
        user.userWatchlist.remove(listing)
    else:
        user.userWatchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", kwargs={'category_name':listing.category,'listing_id':listing.id}))

@login_required(login_url='login')
def watchlist_view(request):
    user = request.user
    watchlist = user.userWatchlist.all()
    onWatchlist = True
    return render(request, "auctions/userAuctions.html",{
        'userAuctions':watchlist,
        'watchlist': onWatchlist,
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def categoryListings(request, category_name):
    category = Category.objects.get(options = category_name)
    listings = category.Filter.exclude(active = False)

    return render(request, "auctions/index.html", {
        "category": category,
        "listings": listings,
    })



class CommentaryForm(ModelForm):
    class Meta:
        model = Commentary
        fields = ['comment']

        widgets = {
            'comment': TextInput(attrs={'class':'form-control', 'placeholder':'Comment'})
        }
        
        labels = {
            'comment':''
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

        widgets = {
            'bid': TextInput(attrs={'class':'form-control', 'placeholder':'Place a bid'})
        }
        
        labels = {
            'bid':''
        }

def listing(request,category_name,listing_id):

    listing = Listing.objects.get(pk = listing_id)
    user = request.user.id
    watchlistBool=False
    comments = listing.Comments.all()

    higherBid = listing.ListingHigherBid.all().last()
    if higherBid is None:
        higherBidNumber = listing.bid
    else:
        higherBidNumber = listing.ListingHigherBid.all().last().bid

    bidsSoFar = listing.ListingHigherBid.all().count()
    winner = listing.winner 

    if User.objects.filter(pk=user).exists():
        userLogged = request.user

        if userLogged.userWatchlist.filter(pk=listing.id).exists():
            watchlistBool = True
        else:
            watchlistBool = False

        if request.method == 'POST' and 'commentBtn' in request.POST: 

            commentForm = CommentaryForm(request.POST)
            if commentForm.is_valid():
                newComment = commentForm.save(commit=False)
                newComment.user = request.user
                newComment.listing = listing
                newComment.save()
                return HttpResponseRedirect(reverse("listing", kwargs={'category_name': listing.category,'listing_id':listing.id})) 
            else:
                return render(request, "auctions/listing.html",{
                    "commentForm":commentForm,
                })

        if request.method == 'POST' and 'bidBtn' in request.POST:
            bidForm = BidForm(request.POST or None)
            if bidForm.is_valid():
                bid = bidForm.cleaned_data['bid']     
                if bid > higherBidNumber:  
                    newBid = bidForm.save(commit = False)
                    newBid.user = request.user
                    newBid.listing = listing
                    newBid.save()
                    return HttpResponseRedirect(reverse("listing", kwargs={'category_name': listing.category,'listing_id':listing.id}))
                else:
                    error = True
                    return render(request, "auctions/listing.html",{
                    "listing":listing,
                    "onWatchlist":watchlistBool,
                    "commentForm": CommentaryForm(),
                    "bidForm":BidForm(),
                    "comments":comments,
                    "higherBid":higherBid,
                    "bidsSoFar":bidsSoFar,
                    "winner":winner,
                    "higherBidNumber":higherBidNumber,
                    "error": error
                    })
                    
    else:
        return render(request, "auctions/listing.html",{
        "listing":listing,
        "comments":comments,
        "higherBid":higherBid,
        "bidsSoFar":bidsSoFar,
        })

    return render(request, "auctions/listing.html",{
        "listing":listing,
        "onWatchlist":watchlistBool,
        "commentForm": CommentaryForm(),
        "bidForm":BidForm(),
        "comments":comments,
        "higherBid":higherBid,
        "bidsSoFar":bidsSoFar,
        "winner":winner,
        "higherBidNumber":higherBidNumber,
    })

@login_required(login_url = 'login')  
def userAuctions(request):
    #user = User.objects.get(pk=user_id) #Este lo usé cuando devolvía el id del usuario
    user = request.user
    auctions = user.UserListings.all()

    return render(request, "auctions/userAuctions.html",{
        "userAuctions":auctions,
    })

@login_required(login_url='login')
def close(request, listing_id):
    user = request.user 
    listing = Listing.objects.get(pk=listing_id)
    bidsSoFar = listing.ListingHigherBid.all().count()
    if listing.user == user and bidsSoFar > 0:
        listing.active = False
        listing.winner = listing.ListingHigherBid.all().last().user
        listing.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'category_name': listing.category,'listing_id':listing.id}))
    else:
        return HttpResponseRedirect(reverse("listing", kwargs={'category_name': listing.category,'listing_id':listing.id}))

@login_required(login_url='login')
def delete(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    if User.objects.filter(pk = user.id).exists() and user == listing.user:
        listing.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("listing", kwargs={'category_name': listing.category,'listing_id':listing.id}))

@login_required(login_url='login')
def won(request):
    user = request.user 
    listings = user.ListingsWon.all()
    won = True
    return render(request, "auctions/userAuctions.html",{
        'userAuctions':listings,
        'won': won,
    }) 