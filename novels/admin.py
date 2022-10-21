from django.contrib import admin
from .models import Novel, NovelShots, Genre, GameMechanic, Developer, Category, Reviews, CourseTheme, CourseSlide, \
    TaskSlide, TaskQuestion, TaskAnswer, QuestionType, TaskBlock, UserSlides, UserAnswer, UserScore, UserTestSlides, \
    SiteNews, Article, ArticleTag, ArticleReviews, CommonReviews, ArticleRating

admin.site.register(Category)
admin.site.register(Novel)
admin.site.register(Genre)
admin.site.register(NovelShots)
admin.site.register(Developer)
admin.site.register(GameMechanic)
admin.site.register(Reviews)

admin.site.register(CourseTheme)
admin.site.register(CourseSlide)
admin.site.register(TaskSlide)
admin.site.register(TaskAnswer)
admin.site.register(TaskQuestion)
admin.site.register(QuestionType)
admin.site.register(TaskBlock)

admin.site.register(UserSlides)
admin.site.register(UserTestSlides)
admin.site.register(UserAnswer)
admin.site.register(UserScore)

admin.site.register(Article)
admin.site.register(ArticleTag)
admin.site.register(SiteNews)
admin.site.register(ArticleReviews)
admin.site.register(CommonReviews)

admin.site.register(ArticleRating)