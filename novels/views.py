import json

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
import services
from .forms import ReviewForm
from . import models

import re

from . import serializers
from .models import UserSlides, UserScore, UserTestSlides, Reviews


class ReviewsList(generics.ListAPIView):
    queryset = models.Reviews.objects.all()
    serializer_class = serializers.ReviewSerializer


class ThemeList(generics.ListAPIView):
    queryset = models.CourseTheme.objects.order_by("number")
    serializer_class = serializers.ThemeSerializer


class NovelsList(generics.ListAPIView):
    queryset = models.Novel.objects.all()
    serializer_class = serializers.NovelSerializer


class CourseSlideList(generics.ListAPIView):
    queryset = models.CourseSlide.objects.all()
    serializer_class = serializers.CourseSlideSerializer


class QuestionList(generics.ListAPIView):
    queryset = models.TaskQuestion.objects.all()
    serializer_class = serializers.QuestionSerializer


class QuestionDetail(generics.RetrieveAPIView):
    queryset = models.TaskQuestion.objects.all()
    serializer_class = serializers.QuestionSerializerDetail


class ScoreList(generics.ListAPIView):
    queryset = models.UserScore.objects.all()
    serializer_class = serializers.UserScoreSerializer


class ScoreDetail(generics.RetrieveAPIView):
    queryset = models.UserScore.objects.all()
    serializer_class = serializers.UserScoreSerializerDetail


class UserAnswerList(generics.ListAPIView):
    queryset = models.UserAnswer.objects.all()
    serializer_class = serializers.UserAnswerSerializer


class UserAnswerDetail(generics.RetrieveAPIView):
    queryset = models.UserAnswer.objects.all()
    serializer_class = serializers.UserAnswerSerializerDetail


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializerDetail


class SlideArrayList(generics.ListAPIView):
    queryset = models.UserSlides.objects.all()
    serializer_class = serializers.SlideArraySerializer


class SlideArrayDetail(generics.RetrieveAPIView):
    queryset = models.UserSlides.objects.all()
    serializer_class = serializers.SlideArraySerializerDetail


class TestSlideList(generics.ListAPIView):
    queryset = models.UserTestSlides.objects.all()
    serializer_class = serializers.TaskSlidesSerializer


class TestSlideDetail(generics.RetrieveAPIView):
    queryset = models.UserTestSlides.objects.all()
    serializer_class = serializers.TaskSlidesSerializerDetail


class TaskSlideList(generics.ListAPIView):
    queryset = models.TaskSlide.objects.all()
    serializer_class = serializers.TaskSlideSerializer


# @api_view(['POST'])
# def add_review(request):
#     print("I'm printing")
#     body = json.loads(request.body.decode('utf-8'))
#     print(body)
#     novel = models.Novel.objects.get(id=body["novel"])
#     review = models.Reviews(email="mail@mail.com", novel=novel, name="userrrrrr", text=body["text"])
#     review.save()
#     return Response({'success': 'ok'})
#
#
# @api_view(['POST'])
# def sign_in(request):
#     body = json.loads(request.body.decode('utf-8'))
#     print(body)
#     user = authenticate(request, username=body["login"], password=body["password"])
#     if user is not None:
#         login(request, user)
#         return Response({'success': 'ok', 'user': body['login']})
#     return Response({'success': 'error', 'errorText': f'Пользователь {body["login"]} не найден!'})
#
#
# @api_view(['POST'])
# def register(request):
#     body = json.loads(request.body.decode('utf-8'))
#     print(body)
#     if len(User.objects.filter(username=body["login"])) > 0:
#         return Response({'success': 'error', 'errorText': f'Пользователь {body["login"]} уже существует!'})
#     user = User.objects.create_user(username=body["login"], password=body["password"])
#     user.save()
#     user = authenticate(request, username=body["login"], password=body["password"])
#     login(request, user)
#     return Response({'success': 'ok', 'user': body['login']})





def user_login(request):
    relocate, template, params = services.auth_services.user_login(request)
    if relocate:
        return redirect(template)
    return render(request, template, params)


def user_logout(request):
    template = services.auth_services.user_logout(request)
    return redirect(template)


@api_view(['POST'])
def add_user_slide(request):
    user = request.user
    code = request.data['slideCode'].replace('#', '').split('/')
    theme = code[0]
    slide_n = code[1]
    if slide_n == "":
        slide_n = 0
    slide_obj = models.CourseTheme.objects.filter(number=int(theme))[0].courseslide_set.filter(number=int(slide_n))
    if len(slide_obj) > 0:
        slides = models.UserSlides.objects.filter(user=user)[0]
        slides.read_slides.add(slide_obj[0])
        slides.save()
        return Response({'success': 'ok'})
    else:
        return Response({'success': 'error'})


def user_registration(request):
    relocate, template, params = services.auth_services.user_registration(request)
    if relocate:
        return redirect(template)
    return render(request, template, params)


def index_view(request):
    return render(request, 'index.html')


def error_view(request):
    referer = request.META.get('HTTP_REFERER')
    return render(request, 'error_template.html', {'redirect_url': referer})


def course_main_view(request):
    return render(request, 'course/course.html')


def profile_main_view(request):
    template, params, user = services.auth_services.change_profile(request)
    request.user = user
    return render(request, template, params)


def profile_progress_view(request):
    return render(request, 'profile/profile_progress.html')


def restore_password_view(request):
    return render(request, 'restore_password.html')


class CourseMainView(ListView):
    model = models.CourseTheme
    queryset = models.CourseTheme.objects.all()


class ThemeDetailView(DetailView):
    model = models.CourseTheme
    slug_field = "number"


def course_lecture(request):
    return render(request, 'course/lecture_3.html')


class NovelView(ListView):
    model = models.Novel
    queryset = models.Novel.objects.filter(draft=False)


class NovelDetailView(DetailView):
    model = models.Novel
    slug_field = "url"


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        novel = models.Novel.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.name = request.user.username
            form.email = request.user.email
            form.novel = novel
            form.save()
        return redirect(novel.get_absolute_url())


def recount_score(user):
    score = models.UserScore.objects.get(user=user)
    questions = models.TaskQuestion.objects.order_by('id')
    temp_score = 0
    for q in questions:
        u_a = models.UserAnswer.objects.filter(user=user).filter(quest_code=q.code).order_by('id')
        if len(u_a) > 0 and u_a[len(u_a) - 1].is_correct and not u_a[len(u_a) - 1].is_cleared:
            temp_score += q.weight
    score.score = temp_score
    score.save()


class AnswerChecker(View):
    def check_test_quest(self, code, user_answers, test_list):
        quest = models.TaskQuestion.objects.get(code=code)
        if not quest.is_auto_check:
            right_answers_numb = [a for a in map(lambda x: str(x.number),
                                                 list(quest.taskanswer_set.filter(is_correct=True)))]
            if quest.type.name == "Ввод слова":
                answer = list(quest.taskanswer_set.all())[0].answer_text
                return str.strip(user_answers[0]) == answer, ""
            return user_answers == right_answers_numb, ""
        else:
            return self.check_script_quest(code, str.strip(user_answers[0]), test_list)

    def post(self, request, pk):
        block = models.TaskBlock.objects.get(id=pk)
        res_dict = {}
        test_list = []
        user = request.user

        for key in request.POST:
            if str.startswith(key, "quest-"):
                q_code = str.replace(key, "quest-", "")
                quest_type = models.TaskQuestion.objects.get(code=q_code).type.name

                answers_list = request.POST.getlist(key)
                print(json.dumps(answers_list))
                answers_list.insert(0, (quest_type == "Ввод слова" or quest_type == "Написание скрипта"))
                # user_answers.update({q_code: answers_list})
                answer_obj = models.UserAnswer(user=user, id_quest=models.TaskQuestion.objects.get(code=q_code),
                                               answers=json.dumps(answers_list[1:]), quest_code=q_code,
                                               is_textvalue=quest_type == "Ввод слова" or quest_type == "Написание скрипта")
                res = self.check_test_quest(q_code, request.POST.getlist(key), test_list)

                answer_obj.is_correct = res[0]
                answer_obj.auto_tests = res[1]
                answer_obj.save()
                if res[0]:
                    res_dict.update({q_code: "Верно"})
                else:
                    res_dict.update({q_code: "Неверно"})
        recount_score(user)
        all_blocks = block.theme.taskblock_set.all()
        all_q = [x for l in [(q.taskquestion_set.all()) for q in all_blocks] for x in l]
        is_done = True
        for q in all_q:
            us_a = models.UserAnswer.objects.filter(user=user).filter(id_quest=q).order_by('id')
            if len(us_a) == 0 or us_a[len(us_a) - 1].is_cleared:
                is_done = False
                break
        if is_done:
            slide = models.UserTestSlides.objects.filter(user=user)[0]
            slide.done_tests.add(block.theme)
            slide.save()
        return redirect(block.url)

    def check_script_quest(self, code, answer, test_list):
        if code == "3_2":
            res = re.search(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', answer)
            if res is not None:
                hex_code = res.group(0)[1:].lower()
                if len(hex_code) == 3:
                    return hex_code == len(hex_code) * hex_code[0], ""
                if len(hex_code) == 6:
                    return hex_code[0:2] * 3 == hex_code, ""
            return False, ""
        elif code == "3_5":
            return check_3_5(answer, test_list)
        elif code == "7_6":
            return check_7_6(answer, test_list)
        return False, ""


def clear_answers(request, pk):
    block = models.TaskBlock.objects.get(id=pk)
    quests = block.taskquestion_set.all().order_by('id')
    for q in quests:
        answers = models.UserAnswer.objects.filter(user=request.user).filter(id_quest=q).order_by('id')
        print(answers)
        if len(answers) > 0:
            print(answers[len(answers) - 1])
            answers[len(answers) - 1].is_cleared = True
            answers[len(answers) - 1].save()

    recount_score(request.user)
    slide = models.UserTestSlides.objects.filter(user=request.user)[0]
    slide.done_tests.remove(block.theme)
    return redirect(block.url)


def check_3_5(answer, test_list):
    test_str = ""
    dict_result = script_analize(answer)
    if len(dict_result['Errors']) > 0:
        for error in dict_result['Errors']:
            test_list.append((False, error))
            test_str += f'{False}*{error};'
            print(test_str)
        return all(map(lambda x: x[0], test_list)), test_str

    test_list.append((len(dict_result['Persons']) == 2, "Количество персонажей"))
    names = sorted(list(map(lambda x: x.name, dict_result['Persons'])))
    test_list.append((names == ["Имя1", "Имя2"], "Соответствие имён персонажей"))
    if len(dict_result['Persons']) > 1:
        test_list.append((str.lower(dict_result['Persons'][0].color) !=
                          str.lower(dict_result['Persons'][1].color), "Заданы разные цвета"))
    test_list.append((len(dict_result['Auth_phrases']) > 0, "Наличие слов автора"))
    test_list.append((len(dict_result['Comments']) > 0 and any(map(lambda x: str.lower(x[1]) == "диалог первый",
                                                                   dict_result['Comments'])), "Наличие комментария"))
    test_list.append((all(map(lambda x: len(x.phrases) > 0, dict_result['Persons'])), "Наличие реплик персонажей"))
    for test in test_list:
        test_str += f'{test[0]}*{test[1]};'
    return all(map(lambda x: x[0], test_list)), test_str


def check_7_6(answer, test_list):
    dict_result = script_analize(answer)
    test_str = ""
    if len(dict_result['Errors']) > 0:
        for error in dict_result['Errors']:
            test_list.append((False, error))
            test_str += f'{False}*{error};'
            print(f'{False}:{error};')
        return all(map(lambda x: x[0], test_list)), test_str
    test_list.append((len(dict_result['Vars']) > 1, "Количество переменных"))
    var_val_end = list(map(lambda x: x[-1][2], dict_result['Vars'].values()))
    test_list.append(("True" in var_val_end and "False" not in var_val_end, "Конечные значения переменных"))
    list_p_if = list(filter(lambda x: str.lower(x[1]) == "я пошёл гулять.", dict_result['Auth_phrases']))
    test_list.append((len(dict_result['If']) > 1 and len(list_p_if) > 0 and
                      list_p_if[0][0] > dict_result['If'][1][0] and list_p_if[0][2] > dict_result['If'][1][1],
                      "Наличие реплики в блоке if"))
    list_p_else = list(filter(lambda x: str.lower(x[1]) == "я остался дома.", dict_result['Auth_phrases']))
    test_list.append((len(dict_result['Else']) > 0 and len(list_p_else) > 0 and
                      list_p_else[0][0] > dict_result['Else'][0][0] and list_p_else[0][2] > dict_result['Else'][0][1],
                      "Наличие реплики в блоке else"))

    for i in range(len(dict_result['If'])):
        v_n = dict_result['If'][i][2]
        n_line = dict_result['If'][i][0]
        v_state = list(filter(lambda x: x[0] < n_line, dict_result['Vars'][v_n]))[-1]
        var_val = v_state[2]
        if i == 0:
            test_list.append((var_val == "True", "Изменение значения переменной"))
        else:
            test_list.append((var_val == "True", "Вывод реплики \"Я пошёл гулять.\""))
    for test in test_list:
        test_str += f'{test[0]}*{test[1]};'
    return all(map(lambda x: x[0], test_list)), test_str


class CharacterObject:
    def __init__(self, var_n, n, c):
        self.var_name = var_n
        self.name = n
        self.color = c
        self.phrases = []


def script_analize(answer):
    a_strings = str.split(answer, "\n")
    result = {"Persons": [], "Comments": [], "Auth_phrases": [], "Labels": [], "Errors": [], "ScriptStart": None,
              "Vars": {}, "Else": [], "If": []}
    define_c = r'^define[ ]+[A-Za-z_]+[A-Za-z0-9_-]*[ ]*=[ ]*Character[ ]*\([ ]*(\"[^\"\n]*\"|\'[^\'\n]*\')[ ]*,[ ]*' \
               r'color[ ]*=[ ]*(\"#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})\"|\'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})\')[ ]*\)[ ]*$'
    pers_phrase = r'^([ ]{4})+[A-Za-z_]+[A-Za-z0-9_-]*[ ]*(\"[^\"\n]*\"|\'[^\'\n]*\'|\'{3}[^\']*\'{3})[ ]*$'
    author_phrase = r'^([ ]{4})+(\"[^\"\n]*\"|\'[^\'\n]*\'|\'{3}[^\']*\'{3})[ ]*$'
    comments = r'^[ ]*#.*$'
    labels = r'^label[ ]+[A-Za-z_]+[A-Za-z0-9_-]*[ ]*:[ ]*$'
    vars_re = r'^define[ ]+[A-Za-z_]+[A-Za-z0-9_-]*[ ]*=[ ]*(\"[^\"\n]*\"|\'[^\'\n]*\'|\'{3}[^\']*\'{3}|True|False|' \
              r'[\d]+)[ ]*$'
    if_re = r'^([ ]{4})+if[ ]+[A-Za-z_]+[A-Za-z0-9_-]*[ ]*:[ ]*$'
    else_re = r'^([ ]{4})+else[ ]*:[ ]*$'
    new_val_re = r'^([ ]{4})+\$[ ]*[A-Za-z_]+[A-Za-z0-9_-][ ]*=[ ]*(\"[^\"\n]*\"|\'[^\'\n]*\'|\'{3}[^\']*\'{3}' \
                 r'|True|False|[\d]+)[ ]*$'
    for i in range(len(a_strings)):
        string = str.replace(a_strings[i], "\r", "")
        if re.search(define_c, string) is not None:
            pers = create_character(string)
            result["Persons"].append(pers)
            if pers.var_name not in result["Vars"].keys():
                result["Vars"][pers.var_name] = []
            result["Vars"][pers.var_name].append((i, "Character", pers.name))

        elif re.search(comments, string) is not None:
            com = str.lstrip(re.search(comments, string).group(0))[1:]
            result["Comments"].append((i, str.lstrip(com)))
        elif re.search(labels, string) is not None:
            label = str.strip(re.search(labels, string).group(0))[5:-1]
            result["Labels"].append((i, str.strip(label)))
            if result["ScriptStart"] is None:
                result["ScriptStart"] = i
        elif re.search(author_phrase, string) is not None:
            phrase = str.strip(re.search(author_phrase, string).group(0))
            if result["ScriptStart"] is None:
                result["Errors"].append(f'Line:{i + 1} У строки есть отступ, но предыдущий оператор его не ожидает')
                break
            elif i > result["ScriptStart"]:
                result["Auth_phrases"].append((i, phrase[1:-1].replace('\'', ''),
                                               (len(string) - len(str.lstrip(string))) // 4))
        elif re.search(pers_phrase, string) is not None:
            temp_str = re.split(r'[\'\"]', str.strip(re.search(pers_phrase, string).group(0)))
            pers_name = str.strip(temp_str[0])
            pers_p = temp_str[1]
            if len(list(filter(lambda x: x.var_name == pers_name, result['Persons']))) > 0:
                pers = list(filter(lambda x: x.var_name == pers_name, result['Persons']))[0]
                pers.phrases.append(pers_p)
            else:
                result["Errors"].append(f'Line:{i + 1} Персонаж {pers_name} не объявлен')
                break
        elif re.search(vars_re, string) is not None:
            var_data = parse_variable(string)
            if var_data[0] not in result["Vars"].keys():
                result["Vars"][var_data[0]] = []
            result["Vars"][var_data[0]].append((i, "Variable", var_data[1]))
        elif re.search(else_re, string) is not None:
            result["Else"].append((i, (len(string) - len(str.lstrip(string))) // 4))
        elif re.search(if_re, string) is not None:
            v_name = parse_if(string)
            if v_name in result["Vars"].keys():
                result["If"].append((i, (len(string) - len(str.lstrip(string))) // 4, v_name))
            else:
                result["Errors"].append(f'Line:{i + 1} Переменная {v_name} не объявлена')
                break
        elif re.search(new_val_re, string) is not None:
            print(string)
            v_data = parse_new_val(string)
            if v_data[0] in result["Vars"].keys():
                result["Vars"][v_data[0]].append((i, "Variable", v_data[1]))
            else:
                result["Errors"].append(f'Line:{i + 1} Переменная {v_data[0]} не объявлена')
                break
    print(result["Vars"])
    tec_check(result)
    return result


def tec_check(dict_res):
    key_words = ["at", "define", "label", "True", "False", "if", "elif", "else", "while", "menu", "show", "hide",
                 "with", "scene", "stop", "play", "call", "expression", "image", "init", "jump", "onplayer", "pass",
                 "python", "return", "set"]
    if len(list(filter(lambda x: x[1] == "start", dict_res['Labels']))) == 0:
        dict_res["Errors"].append("Нет точки входа - отсутствует label start")
    if len(dict_res["Else"]) > 0:
        if len(dict_res["If"]) <= 0 or dict_res["If"][-1][1] != dict_res["Else"][0][1]:
            dict_res["Errors"].append("Нет соответствующего блока if")


def parse_if(full_string):
    return str.strip(str.strip(full_string)[2:-1])


def parse_new_val(full_string):
    str_parts = str.strip(full_string)[1:].split('=')
    return str.strip(str_parts[0]), str.strip(str_parts[1])


def parse_variable(full_string):
    var_name = re.search(r'^define[ ]+[A-Za-z_]+[A-Za-z0-9_-]*[ ]*=', full_string)
    var_name = str.strip(var_name.group(0)[6:-1])
    value = re.search(r'[ ]*(\"[^\"\n]*\"|\'[^\'\n]*\'|\'{3}[^\']*\'{3}|True|False|[\d]+)[ ]*', full_string)
    value = str.strip(value.group(0))
    return var_name, value


def create_character(full_string):
    var_name_temp = re.search(r'^define[ ]+[A-Za-z_]+[A-Za-z0-9_-]*[ ]*=', full_string)
    var_name = str.strip(var_name_temp.group(0)[6:-1])
    name_temp = re.search(r'\([ ]*(\".*\"|\'.*\')[ ]*,', full_string).group(0)
    name = str.strip(name_temp[1:-1])[1:-1]
    color_pers = re.search(r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', full_string).group(0)
    return CharacterObject(var_name, name, color_pers)
