from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from novels.models import UserSlides, UserScore, UserTestSlides, UserSubscription


def user_login(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["login"], password=request.POST["password"])
        if user is not None:
            if request.POST.get("remember") is None:
                request.session.set_expiry(0)
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
        email = str.lower(request.POST['email'])
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
            subscription = UserSubscription()
            subscription.user = user
            subscription.is_subscribed = request.POST.get("subscribe") is not None
            subscription.save()
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


def change_login(request):
    username = request.POST['login']
    if str.strip(username) != '':
        if len(User.objects.filter(username=username)) > 0:
            if request.user.username == username:
                return 'profile/profile_info.html', {
                    'invalid_login': f'Введите новое имя пользователя'}, request.user
            else:
                return 'profile/profile_info.html', {'invalid_login': f'Пользователь {username} уже существует',
                                                     'input_val': username}, request.user
        user = User.objects.filter(username=request.user.username)[0]
        user.username = username
        user.save()
        return 'profile/profile_info.html', {'invalid_login': 'Имя пользователя успешно изменено'}, user
    else:
        return 'profile/profile_info.html', {'invalid_login': "Имя пользователя не может быть пустым"}, request.user


def change_password(request):
    old_password = request.POST['old-password']
    new_password = request.POST['new-password']
    new_password2 = request.POST['new-password-2']
    if str.strip(old_password) != '' and str.strip(new_password) != '' and str.strip(new_password2) != '':
        if len(User.objects.filter(username=request.user.username)) > 0:
            user = authenticate(request, username=request.user.username, password=old_password)
            if user is None:
                return 'profile/profile_info.html', {'invalid_old_password': 'Неверный пароль'}, request.user
            else:
                user.set_password(new_password)
                user.save()
                login(request, user)
                return 'profile/profile_info.html', {'invalid_old_password': 'Пароль успешно изменен'}, user
    else:
        return 'profile/profile_info.html', {'invalid_old_password': "Пароль не может быть пустым"}, request.user


def change_email(request):
    email = str.lower(request.POST['email'])
    if str.strip(email) != '':
        if len(User.objects.filter(email=email)) > 0:
            if request.user.email == email:
                return 'profile/profile_info.html', {
                    'invalid_email': f'Введите новый E-mail'}, request.user
            else:
                return 'profile/profile_info.html', {'invalid_email': f'Пользователь с E-mail {email} уже существует',
                                                     'input_email': email}, request.user
        user = User.objects.filter(username=request.user.username)[0]
        user.email = email
        user.save()
        return 'profile/profile_info.html', {'invalid_email': 'E-mail успешно изменен'}, user
    else:
        return 'profile/profile_info.html', {'invalid_email': "E-mail не может быть пустым"}, request.user


def change_profile(request):
    if request.method == "POST":
        if request.POST.get('login', None) is not None:
            return change_login(request)
        elif request.POST.get('email', None) is not None:
            return change_email(request)
        elif request.POST.get('old-password', None) is not None and request.POST.get('new-password', None) \
                and request.POST.get('new-password-2', None):
            return change_password(request)
        else:
            return 'profile/profile_info.html', {'invalid_old_password': None}, request.user
    else:
        return 'profile/profile_info.html', {'invalid_login': None}, request.user
