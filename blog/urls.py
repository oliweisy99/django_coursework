from . import views
from django.conf import settings # new
from django.urls import path  # new
from django.conf.urls.static import static # new
app_name='blog'
urlpatterns=[
    path('', views.BlogListView.as_view(), name='all'),
    path('bio/', views.BlogBioView.as_view(), name='bio'),
    path('create/', views.BlogCreateView.as_view(), name='create'),
    path('post/<int:pk>/', views.BlogDetailView.as_view(), name='post'),
    path('post/<int:pk>/update/', views.BlogPostUpdateView.as_view(), name='update'),
    path('post/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='delete'),
    path('tempuser/', views.TempUser.as_view(), name='temp_user'),
    path('post/<int:pk>/comment/', views.CreateComment.as_view(), name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.CommentApprove.as_view(), name='comment_approve'),
    path('comment/<int:pk>/remove/', views.CommentRemove.as_view(), name='comment_remove'),
    path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    # path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    # path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    # path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

]


if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)