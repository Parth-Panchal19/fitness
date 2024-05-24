from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponseServerError

# Create your views here.
def checksession(request):
    try:
        uid = request.session['log_id']
        userdata = Login.objects.get(id=uid)

        context = {
            'userdata': userdata,
        }
        return context
    except:
        pass

def diet_info(request):
    diet_data = False  # Assume diet page is not visible by default
    # Check if the user is logged in
    if request.session.get('log_id'):
        # Get the user ID from the session
        user_id = request.session['log_id']
        # Check if there is an active order for the current user
        if Order_table.objects.filter(user_id=user_id, status='complete').exists():
            diet_data = True  # Set to True if there is an active order
    return {'diet_page_visible': diet_data}

def index(request):
    diet1 = diet_info(request)
    return render(request, 'index.html', diet1)

def about(request):
    diet1 = diet_info(request)
    return render(request, 'about.html', diet1)

def grid(request):
    return render(request, 'categories-grid.html')

def customer(request):
    diet1 = diet_info(request)
    return render(request, 'customer.html', diet1)

def insertcustomer(request):
    if request.method == 'POST':
        uid = request.session["log_id"]
        Age = request.POST.get('age1')
        Gender = request.POST.get('gender3')
        Height = request.POST.get('height1')
        Weight = request.POST.get('weight1')
        Dieseas = request.POST.get('disease1')

        insertdata = Customer_Detail(user_id=User_table(id=uid), age=Age, gender=Gender, height=Height, weight=Weight, dieseas=Dieseas)
        insertdata.save()
        return redirect('/list')
    return render(request,'customer.html')

def exerciselist(request):
    exe = Exercise_table.objects.all()
    diet1 = diet_info(request)
    print(exe)
    context = {
        "exe": exe,
        **diet1
    }
    return render(request, 'exerciselist.html', context)

def plans(request):
    plan = SubscriptionPlan_table.objects.all()
    diet1 = diet_info(request)
    context = {
        "plandetails": plan,
        **diet1
    }
    return render(request, "plans.html", context)

def payment(request, id):
    plandata = SubscriptionPlan_table.objects.get(id=id)
    amount = plandata.amount
    diet1 = diet_info(request)
    context = {"plandata": plandata,'amount': amount, **diet1}
    return render(request, 'payment.html', context)

def showpayment(request):
    uid = request.session["log_id"]
    allpayment = payment_table.objects.filter(user_id=uid)
    diet1 = diet_info(request)
    print(allpayment)
    context = {
        "paymentdata": allpayment,
        **diet1
    }
    return render(request,'showpayment.html', context)

def checkpayment(request):
    if request.method == "POST":
        uid = request.session["log_id"]
        planid = request.POST.get('planid')
        # cardName = request.POST.get('cardname')
        cardNumber = request.POST.get('cardnumber')
        cVV = request.POST.get('cvv1')
        Expiry_date = request.POST.get('expirydate')
        amount = request.POST.get('balance1')

        carddata = Card_table.objects.first()
        number = carddata.card_number
        balance = carddata.card_balance
        # Card_Name = carddata.card_name
        ccvv = carddata.cvv
        exdate = carddata.card_expiry_date
        print(number ," ", cardNumber)
        print(cVV," ", ccvv)
        print(Expiry_date, " ", exdate)
        print(amount, " ", balance)

        # uid = 1  # Replace with the actual user ID
        # print(uid)
        # planid = 1  # Replace with the actual plan ID
        # amount = 100.0  # Replace with the actual amount

        if cardNumber == cardNumber and float(amount)<balance and int(cVV) == ccvv:
            if payment_table.objects.filter(user_id=User_table(id=uid)).exists():
                messages.info(request, 'your plan is already active. If Plan will be expired ,you can purchase.')
                return redirect('/plans')
            else:
                import uuid
                trans = str(uuid.uuid4())
                print(trans)

                current_time = timezone.now()

                order = Order_table(user_id=User_table(id=uid), plan_id=SubscriptionPlan_table(id=planid),
                                    status='complete', amount=amount)
                order.save()

                order_id = order.id

                insertpayment = payment_table(user_id=User_table(id=uid), order_id=Order_table(id=order_id), transaction_id=trans, a_amount=amount, time=current_time, status1='complete')
                insertpayment.save()

            messages.success(request, 'Payment is done now complete your profile')
            return redirect('/customer')
        else:
            return render(request, 'index.html')

def list(request):
    uid = request.session["log_id"]
    diet1 = diet_info(request)

    # Fetch user's age and disease from the Customer_Detail model
    customer_info = Customer_Detail.objects.filter(user_id=User_table(id=uid)).first()
    user_age = customer_info.age
    user_disease = customer_info.dieseas

    # Fetch plan_id from the active order of the current user
    active_order = Order_table.objects.filter(user_id=User_table(id=uid), status='complete').first()
    plan_id = active_order.plan_id.id if active_order else None

    # Fetch diet information based on user's age, disease, and plan_id
    diet = DietChart_table.objects.filter(age=user_age, diseases=user_disease, plan_id=plan_id)

    context = {
        "dietdetails": diet,
        **diet1
    }
    return render(request, 'categories-list.html', context)

def contact(request):
    diet1 = diet_info(request)
    return render(request, 'contact.html', diet1)


def signin(request):
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        Username = request.POST.get('name1')
        Emaill = request.POST.get('email1')
        Password = request.POST.get('password1')
        Dob = request.POST.get('dob1')
        Gender = request.POST.get('gender1')
        Phone = request.POST.get('phone1')
        Address = request.POST.get('address1')

        if User_table.objects.filter(email=Emaill).exists():
            messages.info(request, "This email is already registered. Please use another email")
            return redirect(index)
        else:
            insertdata = User_table(u_name=Username, email=Emaill, password=Password, dob=Dob, gender=Gender, mobile=Phone, address=Address)
            insertdata.save()
            messages.info(request, 'your registration has been completed now you can login')
            return redirect(login)

        return render(request, 'signin.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email2']
        password = request.POST['password2']
        try:
            user = User_table.objects.get(email=email, password=password)
            request.session['log_id'] = user.id
            request.session.save()
            messages.success(request, 'Login Successful!!')
            return redirect('/')

        except User_table.DoesNotExist:
            messages.error(request, 'Invalid Email Id and Password')
            return redirect(index)

    return render(request, 'index.html')

def logout(request):
    try:
        del request.session["log_id"]
        messages.success(request, 'Logout Successful!!')
    except:
        pass
    return render(request,"index.html")

def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST.get('email2')
        try:
            user = User_table.objects.get(email=username)

        except User_table.DoesNotExist:
            user = None
        # if user exist then only below condition will run otherwise it will give error as described in else condition.
        if user is not None:
            #################### Password Generation ##########################
            import random

            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            print(password_list)
            random.shuffle(password_list)
            print(password_list)

            password = ""  # we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################

            msg = "hello here it is your new password  " + password  # this variable will be passed as message in mail

            ############ code for sending mail ########################

            from django.core.mail import send_mail

            send_mail(
                'Your New Password',
                msg,
                'parthinfolabz19@gmail.com',
                [username],
                fail_silently=False,
            )
            # NOTE: must include below details in settings.py
            # detail tutorial - https://www.geeksforgeeks.org/setup-sending-email-in-django-project/
            # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            # EMAIL_HOST = 'smtp.gmail.com'
            # EMAIL_USE_TLS = True
            # EMAIL_PORT = 587
            # EMAIL_HOST_USER = 'mail from which email will be sent'
            # EMAIL_HOST_PASSWORD = 'pjobvjckluqrtpkl'   #turn on 2 step verification and then generate app password which will be 16 digit code and past it here

            #############################################

            # now update the password in model
            cuser = User_table.objects.get(email=username)
            cuser.password = password
            cuser.save(update_fields=['password'])

            print('Mail sent')
            messages.info(request, 'mail is sent')
            return redirect(index)

        else:
            messages.info(request, 'This account does not exist')
        return redirect(index)

def changepw(request):
    uid = request.session['log_id']
    if request.method == 'POST':
        cpw = request.POST.get("oldpassword")
        npw = request.POST.get("password")

        cusercheck = User_table.objects.get(id=uid)

        checkpw = cusercheck.password
        print(checkpw)
        print(cpw)

        if checkpw == cpw:
            cuser1 = User_table.objects.get(id=uid)
            cuser1.password = npw
            cuser1.save(update_fields=['password'])
            messages.success(request, 'Password Changed Successfully. ')
        else:
            messages.error(request, 'Current Password is wrong.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def showprofile(request):
    uid = request.session['log_id']
    alluser = User_table.objects.get(id=uid)
    diet1 = diet_info(request)
    context = {'userdata': alluser, **diet1}
    return render(request, 'showprofile.html', context)

def editprofile(request):
    uid = request.session['log_id']
    alluser = User_table.objects.get(id=uid)
    context = {'data': alluser}
    return render(request, 'editprofile.html', context)

def update(request):
    context = checksession(request)
    if request.method == 'POST':
        uid = request.session['log_id']
        name = request.POST.get('name1')
        dob= request.POST.get('dob1')
        address = request.POST.get('address1')
        phone = request.POST.get('phone1')
        object = User_table.objects.get(id=uid)
        object.u_name = name
        object.dob = dob
        object.address = address
        object.mobile = phone

        object.save()
        messages.success(request,'your profile has been completed..')

        return redirect('/showprofile')

    return render(request, 'editprofile.html', context)

def contact(request):
    if request.method == "POST":
        name1 = request.POST.get('name')
        email1 = request.POST.get('email')
        subject1 = request.POST.get('subject')
        message1 = request.POST.get('message')
        address1 = request.POST.get('address')

        if Contact.objects.filter(email=email1).exists():
            messages.info(request, 'you have already filled contact details.')
            return redirect('/contact')
        else:
            contactdata = Contact(name=name1, email=email1, subject=subject1, message=message1, user_address=address1)
            contactdata.save()
            messages.success(request, 'Data added successfully.')
            return redirect('/')
    return render(request, 'contact.html')

def feedback(request):
    uid = request.session['log_id']
    diet1 = diet_info(request)
    if request.method == 'POST':
        ratings1 = request.POST.get('ratings')
        comment = request.POST.get('comment')
        # Assuming you have a Feedback model
        feedbackdata = Feedback(user_id=User_table(id=uid), ratings=ratings1, comment=comment)
        feedbackdata.save()

        messages.success(request, 'Feedback submitted successfully.')
        return redirect('/')

    # Render the feedback form on GET request
    return render(request, 'feedback.html', diet1)
