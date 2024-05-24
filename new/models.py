from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.

user_status = [
    ('active', 'Active'),
    ('expired', 'Expired'),
]

order_status = [
    ('placed', 'placed'),
    ('pending', 'pending'),
    ('complete', 'complete'),
]

diseases = [
    ('obesity', 'obesity'),
    ('cholesterol', 'cholesterol'),
    ('Heart health', 'Heart health'),
    ('Acidity', 'Acidity'),
    ('Blood Pressure', 'Blood Pressure'),
    ('Diabetes', 'Diabetes'),
    ('None', 'None'),
]

customer_age = [
    ('10-25', '10-25'),
    ('25-40', '25-40'),
    ('40-55', '40-55'),
    ('55-70', '55-70'),
]

diet_type = [
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Breakfast', 'Breakfast'),
]
class User_table(models.Model):
    u_name = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    dob = models.DateField()
    gender = models.CharField(max_length=20)
    mobile = models.BigIntegerField()
    address = models.TextField()

    def __str__(self):
        return self.u_name

class Customer_Detail(models.Model):
    user_id = models.ForeignKey(User_table, on_delete=models.CASCADE)
    age = models.CharField(max_length=30, choices=customer_age)
    gender = models.CharField(max_length=30)
    height = models.FloatField()
    weight = models.FloatField()
    dieseas = models.CharField(max_length=30, choices=diseases)

class Exercise_table(models.Model):
    e_name = models.CharField(max_length=30)
    e_description = models.TextField()
    e_image = models.FileField(upload_to='photos', default='')
    calories_burned_per_minute = models.FloatField()

    def exercise_photo(self):
        return mark_safe('<img src = "{}" width="100" />'.format(self.e_image.url))
    exercise_photo.allow_tags = True

class SubscriptionPlan_table(models.Model):
    plan_name = models.CharField(max_length=20)
    duration = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=user_status)
    payment_method = models.CharField(max_length=20)
    amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    desc = models.CharField(max_length=3000)

    def __str__(self):
        return self.plan_name

class DietChart_table(models.Model):
    plan_id = models.ForeignKey(SubscriptionPlan_table, on_delete=models.CASCADE)
    d_type = models.CharField(max_length=20, choices=diet_type, default='Lunch')
    d_name = models.CharField(max_length=50)
    food_name = models.CharField(max_length=20, default='')
    d_image = models.ImageField(upload_to='photos', default='')
    d_description = models.TextField()
    age = models.CharField(max_length=20, choices=customer_age, default='')
    diseases = models.CharField(max_length=30, choices=diseases, default='')
    d_created_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.d_name

    def diet_photo(self):
        return mark_safe('<img src = "{}" width="100" />'.format(self.d_image.url))
    diet_photo.allow_tags = True

class Card_table(models.Model):
    user_id = models.ForeignKey(User_table, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=30)
    card_number = models.CharField(max_length=16, default="")
    cvv = models.IntegerField()
    card_expiry_date = models.CharField(max_length=20, default='')
    card_balance = models.FloatField()

class Order_table(models.Model):
    user_id = models.ForeignKey(User_table, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(SubscriptionPlan_table, on_delete=models.CASCADE)
    add = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=order_status ,default="")
    amount = models.FloatField()

class payment_table(models.Model):
    order_id = models.ForeignKey(Order_table, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User_table, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=10)
    status1 = models.CharField(max_length=20, choices=order_status, default='')
    time = models.DateTimeField()
    a_amount = models.FloatField()

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=11)
    message = models.TextField()
    user_address = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    user_id = models.ForeignKey(User_table, on_delete=models.CASCADE)
    ratings = models.CharField(max_length=30)
    comment = models.CharField(max_length=300, default="")
    timestamp = models.DateTimeField(auto_now=True)