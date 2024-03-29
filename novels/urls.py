from django.urls import path
from . import views


urlpatterns = [
    path('catalog/', views.NovelView.as_view()),
    path('', views.index_view, name="index"),
    path('login/', views.user_login, name='login'),
    path('signin/', views.sign_in, name='sign_in'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name="logout"),
    path('registration/', views.user_registration, name="registration"),
    path('course/', views.course_main_view, name="course_main"),
    path('course/my-theme/', views.course_lecture),
    path('course/<slug:slug>/', views.ThemeDetailView.as_view(), name="theme_detail"),
    path('catalog/<slug:slug>/', views.NovelDetailView.as_view(), name="novel_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("add-review/", views.add_review),
    path("check/<int:pk>/", views.AnswerChecker.as_view(), name="check_answers"),
    path("clear-answers/<int:pk>/", views.clear_answers, name="clear_answers"),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('slides/', views.SlideArrayList.as_view()),
    path('slides/<int:pk>/', views.SlideArrayDetail.as_view()),
    path('courseslides/', views.CourseSlideList.as_view()),
    path('themes/', views.ThemeList.as_view()),
    path('novels/', views.NovelsList.as_view()),
    path('comments/', views.ReviewsList.as_view()),
    path('commontestslides/', views.TaskSlideList.as_view()),
    path('testslide/', views.TestSlideList.as_view()),
    path('testslide/<int:pk>/', views.TestSlideDetail.as_view()),
    path('questions/', views.QuestionList.as_view()),
    path('questions/<int:pk>/', views.QuestionDetail.as_view()),
    path('scores/', views.ScoreList.as_view()),
    path('scores/<int:pk>/', views.ScoreDetail.as_view()),
    path('answers/', views.UserAnswerList.as_view()),
    path('answers/<int:pk>/', views.UserAnswerDetail.as_view()),
    path('add_slide/', views.add_user_slide, name="add_slide"),
]