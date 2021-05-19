from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Listing, User, Category
from django.forms import ModelForm # lo importé para hacer un form a partir de un model definido
from django.contrib.auth.decorators import login_required # lo importé para que solo usuarios registrados accesen a cierta vista

def index(request):
    listings = Listing.objects.filter(active=True) # aqui puedo agregar bool y exclude solo para los activos o filter
    return render(request, "auctions/index.html", {
        "listings": listings,
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
        fields = ['title','description', 'imageURL', 'category', 'bid']


@login_required(login_url = 'login') # esto funciona como un reverse, utiliza un name de los urls definidos para redirigir a los usuarios que no han iniciado sesión
def create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            newListing = form.save(commit=False)  # commit=False Evita que se envíe directo el form ya que falta llenar los datos de usuario
            newListing.user = request.user #Con esto agrego al usuario que hizo la publicación a la DB 
            newListing.save()
            #newListing.save_m2m() # Este lo usaria si agregara datos del tipo ManyToMany
            return render(request, "auctions/create.html",{
                "form":ListingForm()
            })
        else:
            return render(request, "auctions/create.html",{
                "form":form
            })
    return render(request, "auctions/create.html", {
        "form":ListingForm()
    })

def watchlist(request):
    return HttpResponse ("Aquí debe ir la pagina para que el usuario vea su watchlist") 

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

def categoryListings(request, category_id):
    category = Category.objects.get(pk = category_id)
    listings = category.Filter.all()
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings,
    })

def listing(request, category_id, listing_id):
    category = Category.objects.get(pk=category_id)
    listing = Listing.objects.get(pk = listing_id)
    return render(request, "auctions/listing.html",{
        "listing":listing,
    })