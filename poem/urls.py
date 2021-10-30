from django.urls import path

from . import views

urlpatterns = [
    path('', views.PoemsView.as_view(), name='poems'),
    path('<int:pk>', views.PoemDetailView.as_view(), name='retrieve_poem'),
    path('<int:pk>/update', views.PoemUpdateView.as_view(), name='update_poem'),
    path('<int:poem_id>/like', views.like_poem),
    path('<int:poem_id>/dislike', views.dislike_poem),
    path('<int:poem_id>/comment', views.comment_poem, name='comment'),
]
