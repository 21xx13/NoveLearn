from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views
from .forms import UserPasswordResetForm, UserSetPasswordForm

urlpatterns = [
    path('catalog/', views.NovelView.as_view()),
    path('articles/', views.ArticleView.as_view()),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name="article_detail"),
    path('news/', views.SiteNewsView.as_view(), name="news"),
    path('news/<slug:slug>/', views.SiteNewsDetailView.as_view(), name="sitenews_detail"),
    path('', views.index_view, name="index"),
    # path('search/', views.tag_search, name="search"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name="logout"),
    path('registration/', views.user_registration, name="registration"),
    path('course/', views.course_main_view, name="course_main"),
    path('profile/', views.profile_main_view, name="profile_main"),
    path('profile-progress/', views.profile_progress_view, name="profile_progress"),
    path('course/my-theme/', views.course_lecture),
    path('not-existing-path/', views.error_view, name="not_exist"),
    path('course/<slug:slug>/', views.ThemeDetailView.as_view(), name="theme_detail"),
    path('catalog/<slug:slug>/', views.NovelDetailView.as_view(), name="novel_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("article-review/<int:pk>/", views.AddArticleReview.as_view(), name="add_article_review"),
    path("lecture-review/<int:pk>/", views.AddLectureReview.as_view(), name="add_lecture_review"),
    path("task-review/<int:pk>/", views.AddTaskReview.as_view(), name="add_task_review"),
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
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        form_class=UserPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name="registration/password_reset_confirm.html",
                form_class=UserSetPasswordForm
            ), name='password_reset_confirm'),
    path(r'password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         {'template_name': "users/registration/password_reset_complete.html"}, name='password_reset_complete'),
    path("robots.txt",
         TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]
