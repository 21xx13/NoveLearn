from django.contrib.auth.models import User
from django.db import models
from datetime import date

from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class GameMechanic(models.Model):
    """Игровые механики"""
    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Игровая механика"
        verbose_name_plural = "Игровые механики"


class Developer(models.Model):
    """Разработчик"""
    name = models.CharField("Название", max_length=100)
    found_date = models.PositiveSmallIntegerField("Дата основания", default=2022)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="developers/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Разработчик"
        verbose_name_plural = "Разработчики"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Novel(models.Model):
    """Новелла"""
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="novels/")
    developers = models.ManyToManyField(Developer, verbose_name="разработчики", related_name="novel_developer")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    mechanics = models.ManyToManyField(GameMechanic, verbose_name="механики")
    release_date = models.DateField("Дата выхода", default=date.today)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    video_url = models.URLField("Ссылка на трейлер")

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("novel_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Новелла"
        verbose_name_plural = "Новеллы"


class NovelShots(models.Model):
    """Скриншоты из новеллы"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="novel_shots/")
    novel = models.ForeignKey(Novel, verbose_name="Новелла", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Скриншот из новеллы"
        verbose_name_plural = "Скриншоты из новеллы"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    novel = models.ForeignKey(Novel, verbose_name="новелла", on_delete=models.CASCADE)
    publish_date = models.DateTimeField("Время публикации", default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.novel}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class CourseTheme(models.Model):
    """Темы"""
    name = models.CharField("Название", max_length=100)
    number = models.PositiveSmallIntegerField("Номер", default=1, unique=True)
    has_practice = models.BooleanField("Наличие тестов", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class CourseSlide(models.Model):
    """Слайды"""
    name = models.CharField("Название", max_length=100)
    number = models.PositiveSmallIntegerField("Номер", default=1)
    weight = models.PositiveSmallIntegerField("Вес", default=1)
    html_layout = models.TextField("Верстка")
    theme = models.ForeignKey(CourseTheme, verbose_name="Тема", on_delete=models.CASCADE)
    is_practice = models.BooleanField("Практика", default=False)

    def __str__(self):
        return self.name

    def get_review(self):
        return self.commonreviews_set.filter(parent__isnull=True)

    def get_absolute_url(self):
        return f'/course/{self.theme.number}/#{self.number}'

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"


class TaskSlide(models.Model):
    """Слайды с тестами"""
    name = models.CharField("Название", max_length=100)
    number = models.PositiveSmallIntegerField("Номер", default=0)
    theme = models.ForeignKey(CourseTheme, verbose_name="Тема", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_review(self):
        return self.commonreviews_set.filter(parent__isnull=True)

    def get_absolute_url(self):
        return f'/course/{self.theme.number}/#{self.number}'

    class Meta:
        verbose_name = "Слайд с тестом"
        verbose_name_plural = "Слайды с тестами"


class TaskBlock(models.Model):
    """Блоки с вопросами"""
    name = models.CharField("Название", max_length=100)
    number = models.PositiveSmallIntegerField("Номер", default=0)
    theme = models.ForeignKey(TaskSlide, verbose_name="Слайд", on_delete=models.CASCADE)
    is_code_block = models.BooleanField("Блок для автопроверки", default=False)
    url = models.CharField("Адрес блока", max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блок теста"
        verbose_name_plural = "Блоки теста"


class QuestionType(models.Model):
    """Тип задания"""
    name = models.CharField("Тип задания", max_length=150)
    description = models.TextField("Описание", default="Новый тип")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип задания"
        verbose_name_plural = "Типы задания"


class TaskQuestion(models.Model):
    """Вопрос в тесте"""
    number = models.PositiveSmallIntegerField("Номер", default=0)
    code = models.CharField("Идентификатор по темам", max_length=32)
    task_header = models.CharField("Текст задания", max_length=150, default="Текст по умолчанию")
    task_text = models.TextField("Расширенный текст", blank=True)
    help_text = models.TextField("Подсказка", blank=True)
    type = models.ForeignKey(QuestionType, verbose_name="Тип", on_delete=models.SET_NULL, null=True)
    test = models.ForeignKey(TaskBlock, verbose_name="Блок теста", on_delete=models.CASCADE, null=True)
    weight = models.PositiveSmallIntegerField("Вес", default=1)
    is_auto_check = models.BooleanField("Скрипт для проверки", default=False)

    def __str__(self):
        return self.code

    @staticmethod
    def render_input(code, header, text, weight):
        res = f'<div class="form-group"><label for="quest-{code}"><h5 class="question-text">{header} ({weight} балл)</h5></label>'
        if text != "":
            res += f'<div>{text}</div>'
        res += f'<input type="text" class="form-control input-test quest-common" name="quest-{code}" id="quest-{code}" ' \
               f'placeholder="Введите свой ответ" required></div>'
        return res

    @staticmethod
    def render_radio(code, header, answers, text, weight):
        res = f'<label for="quest-{code}"><h5 class="question-text">{header} ({weight} балл)</h5></label>'
        if text != "":
            res += f'<div>{text}</div>'
        res += f'<div id="quest-{code}" class="quest-common">'
        for answer in answers:
            res += f'<div class="form-check"><input class="form-check-input" type="radio" name="quest-{code}" ' \
                   f'id="answer-{code}-{answer.number}" value="{answer.number}" required><label class="form-check-label"' \
                   f'for="answer-{code}-{answer.number}">{answer.answer_text}</label></div>'
        res += '</div>'
        return res

    @staticmethod
    def render_checkbox(code, header, answers, text, weight):
        res = f'<label for="quest-{code}"><h5 class="question-text">{header} ({weight} балл)</h5></label>'
        if text != "":
            res += f'<div>{text}</div>'
        res += f'<div class="checkbox-group-test quest-common" id="quest-{code}">'
        for answer in answers:
            res += f'<div class="form-check"><input class="form-check-input"  type="checkbox" name="quest-{code}" ' \
                   f'value="{answer.number}" id="answer-{code}-{answer.number}" ><label class="form-check-label" ' \
                   f'for="answer-{code}-{answer.number}">{answer.answer_text}</label></div>'
        res += '<div class="task-alert"><i class="fa fa-exclamation" aria-hidden="true">' \
               '</i> Выберите хотя бы один вариант</div>'
        res += '</div>'
        return res

    def html_render(self):
        if self.type.name == "Множественный выбор":
            return self.render_checkbox(str(self.code), str(self.task_header), self.taskanswer_set.all(),
                                        str(self.task_text), self.weight)
        elif self.type.name == "Единственный выбор":
            return self.render_radio(str(self.code), str(self.task_header), self.taskanswer_set.all(),
                                     str(self.task_text), self.weight)
        elif self.type.name == "Ввод слова":
            return self.render_input(str(self.code), str(self.task_header),
                                     str(self.task_text), self.weight)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class TaskAnswer(models.Model):
    """Ответ на вопрос"""
    number = models.PositiveSmallIntegerField("Номер", default=0)
    answer_text = models.TextField("Текст ответа")
    is_correct = models.BooleanField("Верный ответ", default=False)
    question = models.ForeignKey(TaskQuestion, verbose_name="Вопрос", on_delete=models.CASCADE, null=True)

    error_text = models.TextField("Замечание при ошибке", blank=True)
    correct_text = models.TextField("Пояснение при верном ответе", blank=True)

    def __str__(self):
        return f'{self.question.code} - {self.number} - {self.answer_text}'

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class UserScore(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="score")
    score = models.SmallIntegerField("Баллы за задачи", default=0)

    class Meta:
        verbose_name = "Баллы за задачи"
        verbose_name_plural = "Баллы за задачи"


class UserSlides(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="slides")
    read_slides = models.ManyToManyField(CourseSlide, verbose_name="Прочитанные лекции", related_name="read_slides",
                                         blank=True)

    class Meta:
        verbose_name = "Прочитанные слайды"
        verbose_name_plural = "Прочитанные слайды"


class UserTestSlides(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="task_slides")
    done_tests = models.ManyToManyField(TaskSlide, verbose_name="Сделанные тесты", related_name="done_tests",
                                        blank=True)

    class Meta:
        verbose_name = "Страницы тестов"
        verbose_name_plural = "Страницы тестов"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)
    id_quest = models.ForeignKey(TaskQuestion, verbose_name="Вопрос", on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField("Верно", default=False)
    quest_code = models.CharField("Код вопроса", max_length=20, null=True)
    is_textvalue = models.BooleanField("Ввод текста", default=False)
    answers = models.JSONField(null=True)
    auto_tests = models.TextField("Автотесты", default="")
    is_cleared = models.BooleanField("Очищено", default=False)

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователя"


class SiteNews(models.Model):
    title = models.CharField("Заголовок", max_length=150, null=False)
    draft = models.BooleanField("Черновик", default=True)
    html_layout = models.TextField("Верстка")
    publish_date = models.DateTimeField("Время публикации", default=timezone.now)
    url = models.SlugField(max_length=130, unique=True)

    def get_absolute_url(self):
        return reverse("sitenews_detail", kwargs={"slug": self.url})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class ArticleTag(models.Model):
    """Тэг"""
    name = models.CharField("Название", max_length=100)
    color = models.CharField("Цвет", max_length=7)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Тэг статьи"
        verbose_name_plural = "Тэги статей"


class Article(models.Model):
    title = models.CharField("Название статьи", max_length=150, null=False)
    summary = models.CharField("Описание статьи", max_length=500, default="Описание статьи")
    draft = models.BooleanField("Черновик", default=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(ArticleTag, verbose_name="Теги")
    min_read_time = models.PositiveSmallIntegerField("Время на чтение минимум (в минутах)", default=1)
    max_read_time = models.PositiveSmallIntegerField("Время на чтение максимум (в минутах)", default=1)
    html_layout = models.TextField("Верстка")
    publish_date = models.DateTimeField("Время публикации", default=timezone.now)
    create_date = models.DateTimeField("Время создания", default=timezone.now)
    poster = models.ImageField("Обложка", upload_to="articles/", null=True)
    url = models.SlugField(max_length=130, unique=True, null=True)

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.articlereviews_set.filter(parent__isnull=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
 
   
class ArticleReviews(models.Model):
    """Отзывы к статье"""
    user = models.ForeignKey(User, verbose_name="автор", on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    article = models.ForeignKey(Article, verbose_name="новелла", on_delete=models.CASCADE)
    publish_date = models.DateTimeField("Время публикации", default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.article}"

    class Meta:
        verbose_name = "Отзыв к статье"
        verbose_name_plural = "Отзывы к статье"


class CommonReviews(models.Model):
    """Отзывы к темам курса"""
    user = models.ForeignKey(User, verbose_name="автор", on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    course_slide = models.ForeignKey(CourseSlide, verbose_name="страница курса", on_delete=models.CASCADE, null=True)
    task_slide = models.ForeignKey(TaskSlide, verbose_name="страница курса", on_delete=models.CASCADE, null=True)
    publish_date = models.DateTimeField("Время публикации", default=timezone.now)

    def __str__(self):
        return f"{self.user} - отзыв к курсу - {self.publish_date}"

    class Meta:
        verbose_name = "Отзыв к курсу"
        verbose_name_plural = "Отзывы к курсу"


class ArticleRating(models.Model):
    user = models.ForeignKey(User, verbose_name="пользователь", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="Статья", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField("Оценка", default=0)

    def __str__(self):
        return f"{self.user} - {self.article} - {self.rating}"

    class Meta:
        verbose_name = "Оценка статьи"
        verbose_name_plural = "Оценки статьи"
