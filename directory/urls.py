from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'directory'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('login/', auth_views.login, {'template_name': 'directory/login.html'}, name='login'),
    path("logout/", views.LogOutUser, name="logout"),
    path("createAccount/", views.CreateUser.as_view(), name="CreateAccount"),
    
    ## Queries Icecreams Table by field and value
    path('icecreams/<str:name>/<str:flavor>/<str:kin>/<str:style>/<str:price>', views.QueryIce.as_view(), name = "queryice"),
    
    
    ## Look up comments by  User or Ice cream
    path('comments/<str:field>/<str:value>', views.QueryComments.as_view(), name = "querycomments"),

    path('comment/', views.QueryComments.as_view(), name="update_comment"),

    ## Get a user's comment on a specific icecream 
    path('query/user/icecreamcomments/<int:user>/<int:icecream>', views.GetUserCommentOnIceCream.as_view(), name = "query_user_icecream_comments"),

    ## Get user's favorite icecreams
    path('query/user/triedicecream/<int:user>/<str:field>', views.GetUserTried.as_view(), name = "query_user_icecream_favorites"), 

    path('details/<int:pk>/<str:frompg>', views.IcecreamDetails.as_view(), name="itemdetails"),

    path('update/', views.UpdateSavedIcecream.as_view(), name="update_saved"),
    
]	
