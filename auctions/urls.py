from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlist",views.createlist,name="createlist"),
    path('category', views.choosecategory,name="choosecategory"),
    path('thelist/<int:list_id>/', views.thelist, name="thelist"),
    path('removewatchlist/<int:list_id>', views.removewatchlist, name="removewatchlist"),
    path('AddWatchList/<int:list_id>', views.AddWatchList, name='AddWatchList'),
    path('watchlist', views.watchlist, name="watchlist"),
    path('addcomment/<int:list_id>', views.addcomment, name="addcomment"),
    path('addbid2/<int:list_id>', views.addbid2, name="addbid2"),
    path('closeauction/<int:list_id>', views.closeauction, name="closeauction"),


]
