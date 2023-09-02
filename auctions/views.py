from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import User, Category,AuctionListings,Comments, Bids


def index(request):
    alllists=AuctionListings.objects.filter(active=True)
    thecategory = Category.objects.all()
    return render(request, "auctions/index.html",{"allists":alllists, "allcategory":thecategory})


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

def createlist(request):
    if request.method == "GET":
        allthecategories = Category.objects.all()
        return render(request, "auctions/createlist.html", {"allcategory":allthecategories})
    elif request.method == "POST":
        name = request.POST["name"]
        description = request.POST['description']
        price = request.POST['price']
        image = request.POST['image']
        category=request.POST['category']
        thecategory = Category.objects.get(nameofcategory=category)
        theuser= request.user
        thebids = Bids(thebid=int(price),userbid=theuser )
        thebids.save()
        thenewlist = AuctionListings(name=name, description=description,image=image, price=thebids,owner=theuser, category=thecategory)
        thenewlist.save()
        return HttpResponseRedirect(reverse(index))

def thelist(request, list_id):
    thechoosenlist = AuctionListings.objects.get(pk=list_id)
    thelistisinthewatchlist = request.user in thechoosenlist.watchlist.all()
    allcomments = Comments.objects.filter(thelist=thechoosenlist)
    theuser = request.user
    istheowner = theuser.username == thechoosenlist.owner.username
    return render(request, "auctions/thelist.html",{"thelists":thechoosenlist, "thelistisinthewatchlist":thelistisinthewatchlist, "allcomments":allcomments, "istheowner":istheowner})


def choosecategory(request):
    if request.method == "POST":
        thechoosencategory = request.POST['category']
        category = Category.objects.get(nameofcategory=thechoosencategory)
        alllists=AuctionListings.objects.filter(active=True, category=category)
        return render(request, "auctions/category.html",{"allists":alllists})
    

def addbid2(request, list_id):
    TheBid = request.POST['bidss']
    theusers = request.user
    TheChoosenLists = AuctionListings.objects.get(pk=list_id)
    istheowner = theusers.username == TheChoosenLists.owner.username
    if int(TheBid) > TheChoosenLists.price.thebid:
        updatedBid = Bids(userbid=theusers, thebid=int(TheBid))
        updatedBid.save()
        TheChoosenLists.price = updatedBid
        TheChoosenLists.save()
        return render(request, "auctions/thelist.html", {"thelists":TheChoosenLists, "message":"DONE", "UPDATE":True, "istheowner":istheowner})
    else:
        return render(request, "auctions/thelist.html", {"thelists":TheChoosenLists, "message":"ERROR", "UPDATE":False, "istheowner":istheowner})





def AddWatchList(request, list_id):
    thechoosenlist = AuctionListings.objects.get(pk=list_id)
    theuser= request.user
    thechoosenlist.watchlist.add(theuser)
    return HttpResponseRedirect(reverse("thelist", args=(list_id, )))

def removewatchlist(request, list_id):
    thechoosenlist = AuctionListings.objects.get(pk=list_id)
    theuser= request.user
    thechoosenlist.watchlist.remove(theuser)
    return HttpResponseRedirect(reverse("thelist", args=(list_id, )))

def watchlist(request):
    theuser = request.user
    thelists = theuser.watchlist.all()
    return render(request, "auctions/watchlist.html", {"thelists":thelists})



def addcomment(request,list_id):
    theuser= request.user
    thechoosenlist = AuctionListings.objects.get(pk=list_id)
    comment = request.POST['comment']
    TheComment = Comments(commenter=theuser, thelist=thechoosenlist, comments=comment )
    TheComment.save()
    return HttpResponseRedirect(reverse("thelist",args=(list_id, )))

def closeauction(request, list_id):
    thechoosenlist = AuctionListings.objects.get(pk=list_id)
    theuser = request.user
    istheowner = theuser.username == thechoosenlist.owner.username
    thechoosenlist.active = False
    thechoosenlist.save()
    return render(request, "auctions/thelist.html",{"thelists":thechoosenlist, "update":True, "message":"Your Auction Is Closed","istheowner":istheowner})

