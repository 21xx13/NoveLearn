from rest_framework import serializers
from . import models


class CourseSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseSlide
        fields = ['id', 'html_layout']


class ThemeSerializer(serializers.ModelSerializer):
    courseslide_set = CourseSlideSerializer(many=True)
    class Meta:
        model = models.CourseTheme
        fields = ['id', 'name', 'courseslide_set']


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Developer
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ['name']


class NovelShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NovelShots
        fields = ['image']


class NovelSerializer(serializers.ModelSerializer):
    developers = DeveloperSerializer(many=True)
    category = CategorySerializer(many=False)
    genres = GenreSerializer(many=True)
    novelshots_set = NovelShotSerializer(many=True)

    class Meta:
        model = models.Novel
        fields = ['id', 'title', 'description', 'poster', 'developers', 'category', 'genres', 'novelshots_set',
                  'release_date', 'video_url']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = ['id', 'name', 'text', 'email', 'novel']


class TaskSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskSlide
        fields = ['id', 'name']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskQuestion
        fields = ['id', 'weight', 'code']


class QuestionSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.TaskQuestion
        fields = ['id', 'weight', 'code', 'test']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'is_active']


class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'slides', 'useranswer_set', 'score', 'task_slides']


class SlideArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserSlides
        fields = ['id']


class SlideArraySerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.UserSlides
        fields = ['id', 'read_slides']


class TaskSlidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserTestSlides
        fields = ['id']


class TaskSlidesSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.UserTestSlides
        fields = ['id', 'done_tests']


class UserScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserScore
        fields = ['id', 'user']


class UserScoreSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.UserScore
        fields = ['id', 'score', 'user']


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserAnswer
        fields = ['id', 'user', 'is_correct', 'answers', 'quest_code', 'is_cleared', 'is_textvalue', 'id_quest',
                  'auto_tests']


class UserAnswerSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.UserAnswer
        fields = ['id', 'user', 'is_correct', 'answers', 'quest_code', 'is_cleared', 'is_textvalue', 'id_quest']


class ArticleRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleRating
        fields = ['id', 'user', 'article', 'rating']
