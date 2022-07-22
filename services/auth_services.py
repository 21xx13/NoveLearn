from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
        email = request.POST['email']
        if str.strip(username) != '' and str.strip(password) != '':
            if len(User.objects.filter(username=username)) > 0:
                return False, 'registration.html', {'invalid': f'Пользователь {username} уже существует'}
            elif len(User.objects.filter(email=email)) > 0:
                return False, 'registration.html', {'invalid': f'Пользователь с email {email} уже существует'}
            user = User.objects.create_user(username=username, password=password, email=email)
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
