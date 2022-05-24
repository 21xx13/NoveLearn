from django.contrib.auth import authenticate, login, logout
# from novels.models import MainCycle, Boost
from django.contrib.auth.models import User

from novels.forms import UserForm
from novels.models import UserSlides, UserScore, UserTestSlides


def user_login(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["login"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return True, 'index', {}
        else:
            return False, 'login.html', {'invalid': True}
    else:
        return False, 'login.html', {'invalid': False}


def user_logout(request):
    logout(request)
    return 'login'


def user_registration(request):
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']
        if str.strip(username) != '' and str.strip(password) != '':
            if len(User.objects.filter(username=username)) > 0:
                return False, 'registration.html', {'invalid': f'Пользователь {username} уже существует'}
            user = User.objects.create_user(username=username, password=password)
            user.save()
            slides_array = UserSlides()
            slides_array.user = user
            slides_array.save()
            user_score = UserScore()
            user_score.user = user
            user_score.save()
            test_slides = UserTestSlides()
            test_slides.user = user
            test_slides.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return True, 'index', {}

        else:
            return False, 'registration.html', {'invalid': "Имя пользователя и пароль не могут быть пустыми"}
    else:
        return False, 'registration.html', {'invalid': None}
