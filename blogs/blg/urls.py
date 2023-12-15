from django.urls import path
from . import views

urlpatterns = [

    path('signin', views.SignIn.as_view()),
    
    path('blog_tags', views.BlogTagsList.as_view()),
    path('blog_tags/<str:pk>', views.BlogTagsDetail.as_view()),
    
    path('blog_categories', views.BlogCategoriesList.as_view()),
    path('blog_categories/<str:pk>', views.BlogCategoriesDetail.as_view()),
    
    path('blogs', views.BlogsList.as_view()),
    path('blogs/<str:pk>', views.BlogsDetail.as_view()),
    
    path('blog_comments', views.BlogCommentsList.as_view()),
    path('blog_comments/<str:pk>', views.BlogCommentsDetail.as_view()),

]