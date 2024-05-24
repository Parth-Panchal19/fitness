from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('about1', views.about, name='about'),
    path('grid', views.grid, name='grid'),
    path('list', views.list, name='list'),
    path('contact', views.contact, name='contact'),
    path('exerciselist', views.exerciselist, name='exerciselist'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('changepw', views.changepw, name='changepw'),
    path('showprofile', views.showprofile, name='showprofile'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('update', views.update, name='update'),
    path('plans', views.plans, name='plans'),
    path('logout', views.logout, name='logout'),
    path('payment/<int:id>', views.payment, name='payment'),
    path('show', views.showpayment, name='show'),
    path('checkpayment', views.checkpayment, name='checkpayment'),
    path('customer', views.customer, name='customer'),
    path('insertcustomer', views.insertcustomer, name='insertcustomer'),
    path("contact", views.contact, name="contact"),
    path('feedback', views.feedback, name='feedback'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword')
]


