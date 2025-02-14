from django.urls import path, include
# from .views import submit_data
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path("get_cookie", views.get_cookie),
    path('results/', views.results, name='results'),
    path('user_graph/<str:desired_profession>/', views.user_graph, name='user_graph'),
    path('accounts/register/', views.signup, name='signup'),
    path('accounts/login/', views.signin, name='signin'),
    path('get_data/', views.get_skills_data, name='get_data'),
    path('user_roadmap/', views.user_roadmap, name='user_roadmap'),
    path('get_node_hint/', views.get_node_hint, name='get_node_hint'),
    path('gantt-chart/', views.gantt_chart_view, name='gantt_chart'),
    path('gantt-chart-to-excel/', views.gantt_chart_to_excel, name='gantt_chart_to_excel'),
    path('personal_account/', views.personal_account, name='personal_account'),
    path('user_graph_selection/', views.user_graph_selection, name='user_graph_selection'),

   
]
