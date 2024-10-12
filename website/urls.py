from django.urls import path, include
from . import views
from .views import send_mail_page

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('navbar/', views.navbar, name='navbar'),  
    path('search/', views.search, name='search'),    
    path('footer/', views.footer, name='footer'),  
    path('register/', views.register, name='register'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('login/', views.login, name='login'),
    path('login_success/',views.login_success, name='login_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('career/', views.career, name='career'),
    path('organisation_details/', views.organisation_details, name='organisation_details'),
    path('about/', views.about, name='about'),
    path('privacy_policies/', views.privacy_policies, name='privacy_policies'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('menubar/', views.menubar, name='menubar'),
    path('employee_blog/', views.employee_blog, name='employee_blog'),
    path('contactus/', views.contactus, name='contactus'),
    path('mail_sent/', send_mail_page, name='send_mail'),
    path('faq/', views.faq, name='faq'),
    path('job_application/', views.job_application, name='job_application'),
    path('job_application_success/', views.job_application_success, name='job_application_success'),
]
