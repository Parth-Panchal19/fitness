from django.contrib import admin
from .models import *
# Register your models here.

class show_user(admin.ModelAdmin):
    list_display = ['u_name', 'email', 'password', 'dob', 'gender', 'mobile', 'address']

class show_customer(admin.ModelAdmin):
    list_display = ['user_id', 'age', 'gender', 'height', 'weight','dieseas']

class show_exercise(admin.ModelAdmin):
    list_display = ['e_name', 'exercise_photo', 'e_description', 'calories_burned_per_minute']

class show_dietchart(admin.ModelAdmin):
    list_display = ['plan_id', 'd_type', 'd_name','food_name','diet_photo', 'd_description', 'd_created_date','age', 'diseases']


class show_subscription(admin.ModelAdmin):
    list_display = ['plan_name', 'duration', 'status', 'payment_method', 'amount', 'start_date', 'end_date','desc']

class show_card(admin.ModelAdmin):
    list_display = ['card_name', 'card_number', 'cvv', 'card_expiry_date', 'card_balance']

class show_order(admin.ModelAdmin):
    list_display = ['user_id', 'plan_id', 'add', 'status', 'amount']

class show_payment(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'transaction_id', 'status1', 'time', 'a_amount']

class contact_table(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'user_address', 'timestamp']

class feedback_table(admin.ModelAdmin):
    list_display = ['user_id',"ratings", "comment", "timestamp"]

admin.site.register(User_table, show_user)
admin.site.register(Customer_Detail, show_customer)
admin.site.register(Exercise_table, show_exercise)
admin.site.register(DietChart_table ,show_dietchart)
admin.site.register(SubscriptionPlan_table, show_subscription)
admin.site.register(Card_table, show_card)
admin.site.register(Order_table, show_order)
admin.site.register(payment_table, show_payment)
admin.site.register(Contact, contact_table)
admin.site.register(Feedback, feedback_table)


