from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, get_user
from .forms import SignUpForm, LoginForm
from .models import *
import json
import psycopg2
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import plotly.figure_factory as ff
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from plotly.offline import plot
import plotly.express as px
import io
import kaleido


def get_cookie(request):
    # проверяем существование каждой куки, если ее нет, возвращаем пустой список
    skillList = json.loads(request.COOKIES.get("skillList", "[]"))
    selected_professions_2 = json.loads(request.COOKIES.get("selected_professions_2", "[]"))
    profession_dates = json.loads(request.COOKIES.get("profession_dates", "[]"))
    selected_professions = json.loads(request.COOKIES.get("selected_professions", "[]"))
    return skillList, selected_professions_2, profession_dates, selected_professions

def set_profession_cookie(request, profile_profession_id):


    profile_profession = ProfileProfession.objects.get(user_id = profile_profession_id)
   
    profession_name = profile_profession.id_profession.name_profession
    response = HttpResponse("Profession name is set in the cookie")
    response.set_cookie('profession_name', profession_name)
    return response


@login_required
def index(request):
    if request.POST.get('step') == None:
        if request.GET.get('step') == None:
            step = 1
        else:
            step = int(request.GET.get('step'))
    else:
        step = int(request.POST.get('step'))

    if step == 1:




        
        if request.method == 'POST':
            return HttpResponseRedirect('?step=4')

        professions_instance = Profession.objects.all().order_by('id_profession')
        context = {'professions': professions_instance,'step': step}
        response = render(request, 'main/data_input.html', context)
        return response
    
    elif step == 4:
        print('!!!step',step)
        if request.method == 'POST':
            skillList, selected_professions_2, profession_dates, selected_professions = get_cookie(request)
            ID_user = request.user.user_id
            user_instance = main_user.objects.get(user_id=ID_user) 


            if ProfileProfession.objects.filter(user_id=user_instance).exists():
                ProfileProfession.objects.filter(user_id=user_instance).delete()


            for profession_date in profession_dates:
                profession = Profession.objects.get(name_profession=profession_date.split('|')[0])

                profile_profession = ProfileProfession(
                    user_id=user_instance,
                    start_date_work = profession_date.split('|')[1],
                    end_date_work = profession_date.split('|')[2],
                    id_profession =  profession
                )
                profile_profession.save()
            return HttpResponseRedirect('?step=2')

        if 'selected_professions' in request.COOKIES and request.COOKIES['selected_professions'] is not None:
            json_string = request.COOKIES['selected_professions']
            selected_professions = json.loads(json_string)
            print('selected_professions',selected_professions)
        else:
            selected_professions = []
        context = {'selected_professions': selected_professions,'step': step }
        return render(request, 'main/data_input.html', context)
    
    elif step == 3:
        print('!step',step)
        if request.method == 'POST':
            print('Post')
            skillList, selected_professions_2, profession_dates, selected_professions = get_cookie(request)
            ID_user = request.user.user_id
            user_instance = main_user.objects.get(user_id=ID_user) 
            # Delete existing profile, profile_profession, and profile_skill records for the user
            if ProfileSkills.objects.filter(user_id=user_instance).exists():
                ProfileSkills.objects.filter(user_id=user_instance).delete()


            for skill_info in skillList:
                skill_name = skill_info['name'].strip() 
                prof_skill = ProfessionSkill.objects.get(name_skill=skill_name)
                profile_skill = ProfileSkills(
                    user_id=user_instance,
                    id_skill=prof_skill
                )
                profile_skill.save()
                # Check if the profile_skill already exists for the current profile and profession skill
                # existing_profile_skill = ProfileSkills.objects.filter(id_profile=profile, id_skill=prof_skill)
 
            return HttpResponse("Data processed and saved to the database.")



        skills_filtered = ProfessionSkill.objects.filter(Q(for_graph__isnull=True) | Q(for_graph=False))  
        skills_instance = ProfessionSkill.objects.filter(Q(for_graph__isnull=True) | Q(for_graph=False))
        context = { 'skills': skills_instance, 'step': step, 'skills_filtered': skills_filtered,}
        return render(request, 'main/data_input.html', context)
    
    elif step == 2:
        if request.method == 'POST':
            print('Post')
            skillList, selected_professions_2, profession_dates, selected_professions = get_cookie(request)
            ID_user = request.user.user_id
            user_instance = main_user.objects.get(user_id=ID_user) 
            non_empty_selected_professions_2 = [skill for skill in selected_professions_2 if skill]
            # Delete existing profile, profile_profession, and profile_skill records for the user
            if Profile.objects.filter(user_id=user_instance).exists():
                Profile.objects.filter(user_id=user_instance).delete()



            for profession_name in (non_empty_selected_professions_2):
                profession = Profession.objects.get(name_profession=profession_name)
                profile = Profile(
                    user_id=user_instance,
                    desired_profession=profession,
                    about_me="Теперь я в Pichta",
                )
                profile.save()
            return HttpResponseRedirect('?step=3')
        print('!step',step)
        professions_instance = Profession.objects.all().order_by('id_profession')
        context = {'professions': professions_instance,'step': step}
        return render(request, 'main/data_input.html', context)
        


@login_required
def personal_account(request):
    ID_user = request.user.user_id
    user_instance = main_user.objects.get(user_id=ID_user) 
    if Profile.objects.filter(user_id=user_instance).exists() and ProfileSkills.objects.filter(user_id=user_instance).exists() and ProfileProfession.objects.filter(user_id=user_instance).exists():
        prev_professions = ProfileProfession.objects.filter(user_id=user_instance).values_list('id_profession__name_profession', flat=True)
        fut_job_name = Profile.objects.filter(user_id=user_instance).values_list('desired_profession__name_profession', flat=True)
        fut_job_index = Profile.objects.filter(user_id=user_instance).values_list('desired_profession', flat=True)

        skillList = ProfileSkills.objects.filter(user_id=user_instance).values_list('id_skill__name_skill', flat=True)
        professions_list = list(skillList)
        professions_string = ', '.join(professions_list)
        start_date_work = ProfileProfession.objects.values_list('start_date_work', flat=True) or "Вы еще не заполнили это поле"
        end_date_work = ProfileProfession.objects.values_list('end_date_work', flat=True) or "Вы еще не заполнили это поле"

        about_me = Profile.objects.values_list('about_me', flat=True).first() or "Вы еще не заполнили это поле"
        sex = main_user.objects.values_list('sex', flat=True).first() or "Вы еще не заполнили это поле"
        date_of_birth = main_user.objects.values_list('date_of_birth', flat=True).first() or "Вы еще не заполнили это поле"

        context = {
            'fut_job': zip(fut_job_index,fut_job_name),
            'skillList': professions_string,
            'date_work': zip(prev_professions,start_date_work, end_date_work),
            'about_me': about_me,
            'sex': sex,
            'date_of_birth': date_of_birth
        }

        if any([prev_professions, fut_job_name, skillList]):
            return render(request, 'main/personal_account.html', context)
        else:
            print('1')
            return index(request)



@login_required
def results(request):
    return render(request, 'main/results.html')

def get_node_hint(request):
    node_id = request.GET.get('node_id')
    id_skill = ProfessionSkill.objects.get(name_skill=node_id)
    # print(id_skill.id_skill)
    node = Node.objects.filter(node_id_param=id_skill.id_skill).first()
    find_node_id = node.node_id
    hint = Hints.objects.filter(node_id=find_node_id).first()
    if hint:
        # print(hint)
        return JsonResponse({'hint_text': hint.hint_text})
    else:
        return JsonResponse({'hint_text': 'No description available'})
    

def get_skill_frequency(skill_name):
    try:
        frequency_statistic = FrequencyStatistics.objects.filter(id_skill_professions__name_skill=skill_name).first()
        if frequency_statistic:
            return frequency_statistic.graph_count
        else:
            return 'x'  # Если статистика не найдена, возвращаем 0 как значение по умолчанию
    except FrequencyStatistics.DoesNotExist:
        return 'x'  # Если происходит ошибка DoesNotExist, также возвращаем 0 как значение по умолчанию



@login_required
def user_graph(request, desired_profession=None):
    user = get_user(request)
    profiles = Profile.objects.filter(user_id=user)

    if profiles.count() > 1 and not desired_profession:
        return redirect('user_graph_selection')
    
    if desired_profession and desired_profession != 'None' :
        profile = Profile.objects.get(user_id=user, desired_profession=desired_profession)
    else:
        profile = profiles.first()
    user_skills = ProfessionSkill.objects.filter(profileskills__user_id=profile.user_id)
    user_desired_profession = profile.desired_profession
    edges_data = Edge.objects.filter(graph_id__id_profession=user_desired_profession)
    nodes_data = Node.objects.filter(graph_id__id_profession=user_desired_profession)

    nodes = []
    for node in nodes_data:
        skill_name = ProfessionSkill.objects.get(id_skill=node.node_id_param).name_skill
        count_frequence = get_skill_frequency(skill_name)
        node_dict = {
            "color": node.node_color_param,
            "id": skill_name,
            "label": f"{skill_name}\n{count_frequence}",
            "shape": "dot",
        }
        if skill_name in [i.name_skill for i in user_skills]:
            node_dict["color"] = "green"
        else:
            node_dict["color"] = "red"
        nodes.append(node_dict)

    edges = []
    for edge in edges_data:
        from_skill_name = ProfessionSkill.objects.get(id_skill=edge.edge_from_param).name_skill
        to_skill_name = ProfessionSkill.objects.get(id_skill=edge.edge_to_param).name_skill
        edges.append({"from": from_skill_name, "to": to_skill_name})

    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)

    context = {
        'nodes_list': nodes,
        'nodes_data': nodes_json,
        'edges_data': edges_json,
    }
    return render(request, 'main/user_graph.html', context)

@login_required
def user_graph_selection(request):    
    # Add logic to handle user's selection of desired profession and redirecting back to user_graph
    if request.method == 'POST':
        selected_profession = request.POST.get('selected_profession')
        return redirect('user_graph', desired_profession=selected_profession)

    # Provide necessary context data for rendering the user_graph_selection.html template
    professions = Profile.objects.filter(user_id=get_user(request)).values_list('desired_profession', flat=True)
    context = {'professions': professions}
    return render(request, 'main/user_graph_selection.html', context)

@login_required
def get_user_data(request):
    user_id = get_user(request).user_id
    profile = Profile.objects.filter(user_id=user_id).first()
    
    if profile:
        desired_profession_id = profile.desired_profession
        user_skills = [i.name_skill for i in ProfessionSkill.objects.filter(profileskills__id_profile=profile)]
        statistics = FrequencyStatistics.objects.filter(id_profession=desired_profession_id).select_related('id_skill_professions__name_skill').order_by('-count_frequency')
        skills_in_order = list(statistics.values_list('id_skill_professions', 'id_skill_professions__name_skill'))

        data = []
        start_date = datetime.now()

        for skill_id, skill_name in skills_in_order:
            duration = SkillDuration.objects.get(id_skill=skill_id).duration_for_beginer
            finish_date = start_date + timedelta(days=duration)
            status = "Complete" if skill_name in user_skills else "Incomplete"
            data.append(dict(Task=skill_name, Start=start_date, Finish=finish_date, Resource=status))
            start_date = finish_date
        df = pd.DataFrame(data)
        colors = {
            'Not Started': 'rgb(220, 0, 0)',
            'Incomplete': (1, 0.9, 0.16),
            'Complete': 'rgb(0, 255, 100)'
        }

        return df, colors
    
@login_required
def user_roadmap(request):
    df, colors = get_user_data(request)
    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                    group_tasks=True)

    # convert it to JSON
    fig_json = fig.to_json()
    print(fig_json)
    return render(request, 'main/layout_user_roadmap.html', {'fig_json' : fig_json})


@login_required
def gantt_chart_view(request):
    df, colors = get_user_data(request)
    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                    group_tasks=True)

    # Генерация изображения в формате PDF
    img_data = fig.to_image(format="pdf", engine="kaleido")
    # img_data = fig.(format="pdf", engine="kaleido")


    # Отправка изображения пользователю
    response = HttpResponse(img_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="gantt_chart.pdf"'
    return response

@login_required
def gantt_chart_to_excel(request):
    df, colors = get_user_data(request)
    # Сохранение DataFrame в файл Excel
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Gantt Chart')
    writer.close()
    output.seek(0)

    # Отправка файла пользователю
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="gantt_chart.xlsx"'
    return response
        

def signup(request):
    if request.COOKIES.get('sessionid') is not None:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Отправка электронной почты
            subject = 'Добро пожаловать на Pichta Dream Tree!'
            message = f'Дорогой {user.username},\n\nСпасибо за регистрацию на нашем сервисе "Pichta Dream Tree". Желаем вам успешного развития!\n\nС уважением,\nКоманда Pichta Dream Tree'
            from_email = 'pichtadreamtree@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            # Авторизация пользователя
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'main/signup.html', {'form': form})


def signin(request):
    if request.COOKIES.get('sessionid') is not None:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.is_valid(), form.errors)
        if form.is_valid():
            cd = form.cleaned_data
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=cd['username'], password=cd['password'])
            print(user)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')  # Замените 'home' на URL вашей домашней страницы

                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        print('1213123')
        form = LoginForm()
    return render(request, 'main/signin.html', {'form': form})


def get_skills_data(request):
    skill = request.GET.get('query')
    skills = ProfessionSkill.objects.values()
    return JsonResponse(list(skills), safe=False)
