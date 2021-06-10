from django.urls import path
from django.conf.urls import url
# from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.sign_up, name='signup'),
    path('login/', views.sign_in, name='sign_in'),
    path('logout/', views.log_out, name='logout'),
    # path('login/home',views.home, name='home'),
    # path('Catagory/<str:s>/Search_Vacancies', Search_From_Skill.as_view()),
    url(r'^login/home/', views.home, name='home'),
    url(r'^sign_in/', views.Sign_in.as_view(), name='signin'),
    url(r'^register/', views.Register.as_view(), name='register'),
    url(r'^activate/', views.Activate_User.as_view(), name='activate'),
    path('user/<int:id>/', views.About_user.as_view(),name='user'),

    url(r'^profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile_page, name='edit_profile'),
    path('edit_profile/<int:id>/', views.edit_profile_page, name='edit_profile_admin'),
    url(r'^user_profile/', views.Profile_User.as_view(), name='profile_user'),
    path('profile_detail/<int:id>/',views.Profile_Detail.as_view(), name='profile_detail'),

    url(r'^vacancy_add/', views.vacancy_add, name='vacancy_add'),
    url(r'^vacancy/', views.Vacancy.as_view(), name='vacancies'),

    # url(r'^cv/', views.go_to_cv, name='cv_add'),
    path('cv/', views.go_to_cv, name='cv_add'),
    url(r'^cv_add/', views.Curriculam_vita.as_view(), name='cv'),
    path('cv/<int:id>/', views.go_to_cv, name='cv_update_admin'),
    
    url(r'^available_jobs/', views.go_to_available_jobs, name='available_jobs'),

    url(r'^job_applications/', views.job_applications, name='job_applications'),

    path('apply_job/<int:id>/',views.Apply_Job.as_view(), name='apply_job'),

    path('user_detail/<int:id>/<int:vacancy>/',views.cv_detail, name='user_detail'),

    path('create_contract/<int:id>/<int:vacancy>/',views.create_contract, name='create_contact'),
    url(r'^contract/', views.Send_Contract.as_view(), name='contract'),
    path('contract_sign/', views.Send_Contract.as_view(), name='contract_sign'),
    path('offers/',views.offer_list, name='offers'),
    path('get_contract/<int:id>/',views.get_contract, name='get_contract'),
    path('search/contract/form/',views.go_to_contract_search, name='search_contract_form'),
    path('search/contract/detail/',views.contract_page_detail, name='search_contract_detail'),

    path('forget_password/', views.forget_password_page, name='forget_password_page'),
    path('forget_password/email/',views.Forget_Password.as_view(), name='forget_password_email'),
    url(r'^forget_password/token/check/',views.Token_Check.as_view(), name='forget_password_token_check'),
    url(r'^forget_password/change/',views.Forget_Password_Change.as_view(), name='forget_password_change'),
    #path('forget_password/email/', views.verify_forget_password_user, name='forget_password_email')

    path('users/',views.go_to_user_detail, name='users'),    
    path('user/update/<int:id>', views.change_user_type, name='change_user_type'),
    path('change_password/',views.go_change_new_password, name='go_change_password'),
    url(r'^change_password/confirm', views.Change_Password.as_view(), name='change_password'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)