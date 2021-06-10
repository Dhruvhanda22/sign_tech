# import the models of python or django 
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
import json
import re 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404 
from django.contrib.auth.hashers import make_password, check_password
import jwt
import datetime
import random
import requests
from django.core.mail import EmailMessage
from django.contrib import messages
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
# Create your views here.

# class to register user api
class Register(APIView):
    # function to get user detail
    def get(self, request):
        data = User_detail.objects.all()
        serializers = User_detailSerilizer(data, many= True)
        return Response(serializers.data)

    # functin to post the user detail
    def post(self, request, format="application/json"):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # get request data
        stream = request.data
        email = stream['email']
        stream['public'] = True
        # validate the user inputs
        if(re.search(regex,email) == None):
            return Response('Invalid email')  
        elif(User_detail.objects.filter(email = email)):
            return Response('Email already exist', status=status.HTTP_200_OK)
        elif( len(stream['password'])<8 ):
            return Response('Password must have more than 8 values')
        elif(re.search("[_@$#!%^&*]", stream['password']) == None):
            return Response('Password is not so strong')
        else:     
            password = make_password(stream['password'])
            stream['password'] = password
            serializers = User_detailSerilizer(data=stream)
            
            if serializers.is_valid():
                msg = send_mail(email = email)
                if msg is None:
                    # save the user detail
                    serializers.save()
                    return Response(serializers.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(msg, status=status.HTTP_200_OK)
                
                
        return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)

# class to change password api
class Change_Password(APIView):
    def post(self, request):
        # check token and authenticate user
        if (check_user(request) == True):
            i = User_detail.objects.get(email = request.session['digita'])
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            re_password = request.POST['re_password']
            # check password is empty
            if (current_password is None or new_password is None or re_password is None):
                return Response('Most have fill the field')
            else:
                # check the current password which is encoded with the input password
                if(check_password(current_password, i.password)):
                    # check new and re password is same or not
                    if new_password == re_password:
                        # check new password length
                        if( len(new_password) < 8):
                            return Response('Password must have more than 8 values')
                        # check new password strength
                        elif(re.search("[_@$#!%^&*]", new_password) == None):
                            return Response('Password is not so strong')
                        else:
                            # set new password
                            i.password = make_password(new_password)
                            i.save()
                            return Response('Successfully change password', status=status.HTTP_200_OK)
                    else:
                        return Response('New and Re Password not matched')
                else:
                    return Response('Current password is not matched')
        else:
            return Response("Session not found", status=status.HTTP_200_OK)

# class to forget password api
class Forget_Password(APIView):
    # function to post the password 
    def post(self, request, format="application/json"):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # get request data
        stream = request.data
        email = stream['email']

        # validation of user input
        if(re.search(regex,email) == None):
            return Response('Invalid email')  
        elif(User_detail.objects.filter(email = email)):
            # send_mail function call to send token on mail
            msg = send_mail(email = email)
            # check return of send_mail
            if msg is None:
                return Response("all good", status=status.HTTP_201_CREATED)
            else:
                return Response(msg, status=status.HTTP_200_OK)
        else:     
            return Response('Email not found')
                
                
        return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)

# class to change the pasword which is forget
class Forget_Password_Change(APIView):
    # when post method call    
    def post(self, request, format="application/json"):
        # get request data
        stream = request.data
        email = stream['email']
        new_password = stream['new_password']
        re_password = stream['re_password']
        # call change pasword function
        soln = change_password(email=email, new_password=new_password, re_password=re_password)
        # chec output boolean
        if soln is True:
            return Response('Successfully change password',status=status.HTTP_200_OK)
        elif soln is False:
            return Response('Server error')
        else:
            return Response(soln)

# class to check the token
class Token_Check(APIView):

    def post(self, request, format="application/json"):
        # get rquest data
        stream = request.data
        email = stream['email']
        token = stream['token']
        # call check_token function
        soln = check_token(email=email,token=token)
        # check return boolean
        if soln is True:
            return Response('Token ok',status=status.HTTP_200_OK)
        elif soln is False:
            return Response('Server Error')
        else:
            return Response(soln)

# class to add vacancy detail api
class Vacancy(APIView):
    # function to get the vacancy detail
    def get(self, request):
        data = Vacancy_Detail.objects.all()
        serializers = Vacancy_detailSerilizer(data, many= True)
        return Response(serializers.data)
    # function to post the vacancy detail 
    def post(self, request):
        i = User_detail.objects.get(email = request.session['digita'])
        stream = request.data
        vacancy_no = stream['vacancy_no']

        # exception handeling 
        # try:
        #     j = User_profile.objects.get(user = i.id)
        # except:
        if i.hdo is True:
            # if new vacancy is added
            if vacancy_no == "":
                value = Vacancy_Detail(
                job_title  = request.POST['job_title'],
                education = request.POST['education'],
                range_of_salary = request.POST['range_of_salary'],
                plus_services = request.POST['plus_services'],
                experience_year = request.POST['experience_year'],
                task_and_responsibilities = request.POST['task_and_responsibilities'],
                qualification_and_experience = request.POST['qualification_and_experience'],
                expiry_date = request.POST['expiry_date'],
                contract_time  = request.POST['contract_time']
                )
                value.save()
                return Response("Sucessfully added vacancy" , status=status.HTTP_201_CREATED)
            else:
                k = Vacancy_Detail.objects.get(id = vacancy_no)
                k.job_title = request.POST['job_title']                
                k.education = request.POST['education']
                k.range_of_salary = request.POST['range_of_salary']
                k.plus_services = request.POST['plus_services']
                k.experience_year = request.POST['experience_year']
                k.task_and_responsibilities = request.POST['task_and_responsibilities']
                k.qualification_and_experience = request.POST['qualification_and_experience']
                k.expiry_date = request.POST['expiry_date']
                k.contract_time  = request.POST['contract_time']
                k.save()
                return Response("Successfully update", status=status.HTTP_200_OK)
        else:
            return Response("You are not authenticate user" , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class to CV api
class Curriculam_vita(APIView):
    # function to get the CV data
    def get(self, request):
        data = User_CV.objects.all()
        serializer = CV_detailSerilizer(data, many= True)
        return Response(serializer.data)

    # function to post the CV data
    def post(self, request):
        if (check_user(request) == True):
            stream = request.data
            user_no = stream['user_no']
            print(user_no)
            if user_no == "":
                k = User_detail.objects.get(email = request.session['digita'])
                if k.public is True:
                    print(k.pk)
                    user_no = k.pk
                else:
                    return Response("User not found", status=status.HTTP_200_OK)
            i = User_detail.objects.get(id = user_no)
            # update the data if it already exist else create it
            if User_CV.objects.filter(user = i.pk).exists():
                k = User_CV.objects.get(user = i.pk)
                k.profession = request.POST['profession']
                k.education = request.POST['education']
                k.skills = request.POST['skills']
                k.experience_detail = request.POST['experience_detail']
                k.reference_name = request.POST['reference_name']
                k.reference_workat = request.POST['reference_workat']
                k.reference_position = request.POST['reference_position']
                k.reference_email = request.POST['reference_email']
                k.reference_contact = request.POST['reference_contact']
                k.save()
                return Response("Successfully update", status=status.HTTP_200_OK)
            value = User_CV(
                user = i,
                profession = request.POST['profession'],
                education = request.POST['education'],
                skills = request.POST['skills'],
                experience_detail = request.POST['experience_detail'],
                reference_name = request.POST['reference_name'],
                reference_workat = request.POST['reference_workat'],
                reference_position = request.POST['reference_position'],
                reference_email = request.POST['reference_email'],
                reference_contact = request.POST['reference_contact']
                )
            value.save()
            return Response("Sucessfully added CV" , status=status.HTTP_200_OK)
            return Response("CV already exist")
        else:
            return Response("Session not found", status=status.HTTP_200_OK)

# class to 
class About_user(APIView):
    def get_object(self, id):
        try: 
            return User_profile.objects.get(id=id)
        except User_profile.DoesNotExist:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        i = self.get_object(id)
        serializer = User_detailSerilizer(i, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        if (check_user(request) == True):
            try:
                i = User_detail.objects.get(email = request.session['digita'])
                if i.admin is True:
                    j = User_detail.objects.get(id = id)
                    j.delete()
                    return Response("Deleted user", status=status.HTTP_200_OK)
                else:
                    return Response("You are not authenticate user", status=status.HTTP_200_OK)
            except:
                return Response("User not found")
        else:
            return Response("Session not found", status=status.HTTP_200_OK)

# class to sign up the user
class Sign_in(APIView):
    def post(self, request):
        stream  = request.data
        email = stream['email']
        password = stream['password']
        try:
            i =  User_detail.objects.get(email = email)
            if(i.active is True):
                if(check_password(password, i.password)):
                    if(i.public is True):
                        user_type = 'public'
                    elif(i.hdo is True):
                        user_type = 'hod'
                    elif(i.admin is True):
                        user_type='admin'
                    encoded_jwt = jwt.encode({'id':i.id,'email': email,'user_type':user_type}, 'secret')
                    request.session['digita'] = email
                    return Response('ok', status=status.HTTP_200_OK)   
                else:
                    return Response("You gave wrong password") 
                return Response("password not matched")
            else:
                if OTP_token.objects.filter(email = email): 
                    return Response("Activate the account", status=status.HTTP_200_OK)
                else:
                    send_mail(email = email)
                    return Response("Activate the account", status=status.HTTP_200_OK)
            
        except User_detail.DoesNotExist:
            return Response("Email is not valid")

        return Response("Request not matched", status=status.HTTP_400_BAD_REQUEST)

# class to activate the user id
class Activate_User(APIView):
    def post(self, request):
        stream = request.data
        tok = stream['token']
        email = stream['email']
        db_tok = ""
        print(email)
        print(tok)
        try:
            i = OTP_token.objects.get(email = email)
            db_tok = i.token
        except:
            return Response("Email not found")
        # check the token exist to activate the account
        if(tok == db_tok):
            j = User_detail.objects.get(email = email)
            # conc.request("PUT","http://127.0.0.1:8000/user/"+str(j.id))
            # return None
            j.active = True
            j.save()
            i.delete()

            return Response("Successfully activate account", status=status.HTTP_200_OK)
        else:
            return Response("Token is not valid")

# class to add and get user profile
class Profile_User(APIView):
    # function to get the user profile
    def get(self, request):
        data = User_profile.objects.all()
        # data = User_profile.objects.get(id = id)
        serializers = Profile_detailSerilizer(data, many= True)
        return Response(serializers.data)
    # function to add update profile
    def post(self, request):
        if (check_user(request) == True):
            i = User_detail.objects.get(email = request.session['digita'])
            stream = request.data
            user_no = i.pk
            if i.admin is True:
                user_no = stream['user_no']
            try:
                j = User_profile.objects.get(user = user_no)
            except:
                value = User_profile(
                    user = i,
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    country = request.POST['country'],
                    city = request.POST['city'],
                    local_place = request.POST['local_place'],
                    contact = request.POST['contact'],
                    date_of_birth = request.POST['date_of_birth'],
                    signature = request.FILES['signature'],
                )
                value.save()
                return Response("Successfully added", status=status.HTTP_200_OK)
                return Response("No valid detail")
            k = User_profile.objects.get(user = user_no)
            k.first_name = request.POST['first_name']
            k.last_name = request.POST['last_name']
            k.country = request.POST['country']
            k.city = request.POST['city']
            k.local_place = request.POST['local_place']
            k.contact = request.POST['contact']
            k.date_of_birth = request.POST['date_of_birth']
            try:
                k.signature = request.FILES['signature']
            except:
                None
            k.save()
            print('aa')
            return Response("Successfully update", status=status.HTTP_200_OK)
        else:
            return Response("Session not found", status=status.HTTP_200_OK)
    # def post(self, request):
    #     serializer = Profile_detailSerilizer(data=request.data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Profile_Detail(APIView):

    def get_object(self, id):
        try: 
            return User_profile.objects.get(id=id)
        except User_profile.DoesNotExist:
            return Response("Not FOund",status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        profile = self.get_object(id)     
        serializer = Profile_detailSerilizer(profile)
        return Response(serializer.data)



    def put(self, request, id):
        profile = self.get_object(id)
        serializer = Profile_detailSerilizer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class to apply job by candidate
class Apply_Job(APIView):
     def get(self, request, id):
        # verify user session
        if (check_user(request) == True): 
            i = User_detail.objects.get(email = request.session['digita'])
            v = Vacancy_Detail.objects.get(id = id)
            # check user profile and cv exist or not
            if (User_profile.objects.filter(user = i).exists() and User_CV.objects.filter(user = i).exists()):
                data = Apply_job.objects.all()
                for j in data:
                    if j.user == i and j.vacancy == v:
                        return Response("You have already applied for this job", status=status.HTTP_200_OK)
                value = Apply_job(
                    user = i,
                    vacancy = v,
                )
                value.save()
                return Response("Successfully Applied", status=status.HTTP_200_OK)
            else:
                return Response("CV or Profile is not created", status=status.HTTP_200_OK)
        else:
            return Response("Session Expire", status=status.HTTP_200_OK)

# class to create contract in pdf
class Send_Contract(APIView):
    def render_to_pdf(self,template_src, context_dict={}):
        html = render_to_string(template_src, {'data':context_dict})
        filename = 'media/'+ context_dict.get("name") + '_' + str(context_dict.get("id")) + str(context_dict.get("c_id")) +'.pdf'
        write_to_file = open(filename, "w+b")

        result = pisa.CreatePDF(html, dest=write_to_file)

        write_to_file.close()

        fs = FileSystemStorage()
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
                return response
        return HttpResponse(result.err)

    # function to create contract
    def post(self, request):
        # verify user session
        if check_user(request) == True:
            i = User_detail.objects.get(email = request.session['digita'])
            user_type = "hod"
            # check the user if hod or not
            if(i.hdo is True):
                value = Contract_detail(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    position = request.POST['position'],
                    contract_time = request.POST['contract_time'],
                    salary = request.POST['salary']
                )
                value.save()
                return Response("Successfully added", status=status.HTTP_200_OK)
            else:
                return Response("You are not authorized user", status=status.HTTP_200_OK)
        else:
            return render(request, 'signin.html')        
    
    # function to update the contract (candidate as signature and admin as update)
    def put(self, request):
        stream = request.data
        print(stream)
        # check user session
        if check_user(request) == True: 
            id = stream['contract_no'] 
            i = User_detail.objects.get(email = request.session['digita'])
            user_type = "public"
            if id is None or id == "":
                return Response("Contract Id not found", status=status.HTTP_200_OK)
            k = Contract_detail.objects.get(id = id)
            if(i.admin is True):
                k.name = request.POST['name']
                k.email = request.POST['email']
                k.position = request.POST['position']
                k.contract_time = request.POST['contract_time']
                k.salary = request.POST['salary']
                k.save()
                return Response("Successfully update the contract", status=status.HTTP_200_OK)
            elif(i.public is True):
                # filter the contract and get the exist contract deatil
                if Contract_detail.objects.filter(email = i.email).exists():
                    # verify signature status
                    if k.signature_bool is True:
                        return Response("You have already sign in this contract", status=status.HTTP_200_OK)
                    try:
                        # get the signature time and encoded in the code generated for signature
                        now = datetime.datetime.now()
                        k.signature_value = jwt.encode({'id':i.id,'email': i.email, 'date_time': now.strftime("%Y-%m-%d %H:%M:%S")}, 'signature confirm')
                    except:
                        return Response("Problem while creating the digital signature", status=status.HTTP_200_OK)
                    # set the sognature status true
                    k.signature_bool = True
                    k.save()
                    contract_user = User_detail.objects.get(email=k.email)
                    user_id = contract_user.pk
                    profile = User_profile.objects.get(user_id = user_id)
                    print(profile.signature)

                    context = {
                        "id":i.pk,
                        "name":i.username,
                        "full_name": str(profile.first_name) + " " + str(profile.last_name),
                        "c_id":id,
                        "email":k.email,
                        "salary":k.salary,
                        "position":k.position,
                        "contract_time":k.contract_time,
                        "signature":profile.signature,
                    }

                    self.render_to_pdf('contract_pdf.html',context)

                    return Response("Contract signed Successfully", status=status.HTTP_200_OK)
                else:
                    return Response("This contract is not found", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response("You are not authorize user", status=status.HTTP_200_OK)

        else:
            return render(request, 'signin.html')  


# function to send the mail to the candidate
def send_mail(email = None):
    # current_site = get_current_site(request) # this function helps to get the presnt host id 
    subject = 'Token from the digital signature account.' # subject to the gmail after sign up
    # set random number in varaible
    message = str(random.randint(999, 9999))
    # check email is None or get
    if(email is None or email == ""):
        return "email is not found"
    elif (message is None or message == ""):
        return "Token problem"
    else:
        # save the token in database as per email
        try:
            i = OTP_token.objects.get(email = email)
            i.token = message
            i.save()
        except:
            values = OTP_token(
            email = email,
            token = message)
            values.save()

        to_email = email # get the email to gmail
        email = EmailMessage(subject, message, to=[to_email]) # call function to email
        email.send() # send email
        return None

# function to log out the user
def log_out(request):
    # check the session
    if('digita' in request.session):
        # delete the session
        del request.session['digita']
        return render(request, 'signin.html')
    else:
        return render(request, 'signup.html')

# function to go the home page
def home(request):
    try:
        # check if session is remain
        if('digita' in request.session):
            # get the user detail from session
            user = request.session['digita']
            user_type = "public"
            try:
                # get email according to user
                i = User_detail.objects.get(email = user)
            except:
                del request.session['digita']
                return render(request, 'signin.html')
            # check user type to go to the page according to user type
            if(i.admin is True):
                user_type = "admin"
                return render(request, 'admin_page.html', {'cond':'auth', 'user_name': i.username, 'user_type':user_type})
            elif(i.hdo is True):
                user_type = "hod"
                return render(request, 'hod_page.html', {'cond':'auth', 'user_name': i.username, 'user_type':user_type})
            else:
                return render(request, 'home.html',{'cond':'auth', 'user_name': i.username, 'user_type':user_type})
        else:
            return render(request, 'signin.html')
    except:
        return render(request, 'signin.html')

# function to get the user profile
def profile(request):
    # verify user session
    if (check_user(request) == True):
        # get user according to session
        i = User_detail.objects.get(email = request.session['digita'])
        user_no = i.id
        user_type = "public"
        if(i.hdo is True):
            user_type = "hod"
        try:
            j = User_profile.objects.get(user = user_no)
        except:
            country = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]   
            # render to the user profile page
            return render(request, 'update_profile.html',{'cond':'auth', 'user_name': i.username, 'user_type': user_type, 'country':country,})
        j = User_profile.objects.get(user = user_no)
        url = 'http://127.0.0.1:8000/profile_detail/'+ str(j.id)
        # check user want to post or get profile
        if request.method == 'POST':
            r = requests.post(url, params=request.POST)
        else:
            r = requests.get(url, params=request.GET)
            a = json.loads(r.text)
            return render(request, 'profile.html',{'cond':'auth', 'v': a, 'user_name': i.username, 'user_type': user_type})
        return HttpResponse('Could not found data')
    else:
        return render(request, 'signin.html')

# function to go the profile page
def edit_profile_page(request,id=None):
    if check_user(request):
        i = User_detail.objects.get(email = request.session['digita'])
        user_type = "public"
        user_no = i.id
        # check if the user is hod
        if(i.hdo is True):
            user_type = "hod"
        if i.admin is True:
            print('ok')
            user_type = "admin"
            user_no = id
            if user_no is None:
                return render(request, 'signin.html')
        country = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]     
        try: 
            j = User_profile.objects.get(user = user_no)
            url = 'http://127.0.0.1:8000/profile_detail/'+str(j.id)
        except:
            return go_to_user_detail(request)
        r = requests.get(url, params=request.GET)
        a = json.loads(r.text)
        return render(request, 'update_profile.html',{'cond':'auth', 'v': a, 'user_name': i.username,'country':country, 'user_type': user_type, 'user_no':user_no})

# function to check user session
def check_user(request):
    # check the request session in browser
    if('digita' in request.session):
        user = request.session['digita']
        # exception handeling
        try:
            i = User_detail.objects.get(email = user)
        except:
            del request.session['digita']
            return render(request, 'signin.html')
        return True
    else:
        return False

# function to go to the sign up page
def sign_up(request):
    # check the session
    if('digita' in request.session):
        i = User_detail.objects.get(email = request.session['digita'])
        user_type = "public"
        if(i.hdo is True):
            user_type = "hod"
        elif(i.admin is True):
            user_type = "admin"
        # render the home page 
        return render(request, 'home.html',{'cond':'auth', 'user_name': request.session['digita'], 'user_type': user_type})
    else:
        return render(request, 'signup.html')

# function to render sign in page
def sign_in(request):
    return render(request, 'signin.html')

# function to render sign up page
def register(request):    
    return render(request, 'signup.html')

# function to render vacancy add page
def vacancy_add(request):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        return render(request, 'vacancy_add.html',{'cond':'auth', 'user_name': i.username, 'user_type':'hod'})
    else:
        return render(request, 'signin.html')

# function to render CV detail
def go_to_cv(request, id=None):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        user_no = i.id
        user_type = "public"
        if i.admin is True:
            user_no = id
            user_type = "admin"
        a=None
        if User_CV.objects.filter(user = user_no).exists():
            j = User_CV.objects.get(user = user_no)
            a = {"user_no":user_no, "education":j.education, "profession":j.profession,"skills":j.skills,"experience_detail":j.experience_detail,"reference_name":j.reference_name,"reference_workat":j.reference_workat,"reference_position":j.reference_position, "reference_email":j.reference_email,"reference_contact":j.reference_contact}
        return render(request, 'add_cv_page.html',{'cond':'auth', 'v':a, 'user_name': i.username, 'user_type':user_type})
    else:
        return render(request, 'signin.html')

# function to render the avialable jobs page
def go_to_available_jobs(request):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        user_type = "public"
        if(i.hdo is True):
            user_type = "hod"
        if(i.admin is True):
            user_type = "admin"
        data = Vacancy_Detail.objects.all()
        return render(request, 'available_jobs.html',{'cond':'auth', 'data':list(data), 'user_name': i.username, 'user_type':user_type})
    else:
        return render(request, 'signin.html')

# function to rrender the job applications apge
def job_applications(request):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        query_set = Apply_job.objects.all()
        data = list(query_set)
        new_list = []
        for j in data:
            # set the data in varaibles
            u = User_detail.objects.get(id = j.user.id)
            v = Vacancy_Detail.objects.get(id = j.vacancy.id)
            p = User_profile.objects.get(user = u.id)
            cv = User_CV.objects.get(user = u.id)
            name = str(p.first_name) + " " + str(p.last_name)
            # add the data of list which required
            new_list.append({'v_id': v.id, 'user_id': u.id, 'name' : name, 'position': v.job_title, 'higher_education' : cv.education})
        user_type = "hod"
        # render in job_applications page
        return render(request, 'job_applications.html',{'cond':'auth','user_name': i.username, 'user_type':user_type, 'data':new_list })
    else:
        return render(request, 'signin.html')

# function to render the view user detail page
def cv_detail(request, id = None, vacancy = None):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        user_type = "hod"
        # get user profile detail
        u = User_profile.objects.get(user = id)
        # get user Cv detail
        cv = User_CV.objects.get(user = id)
        name = str(u.first_name) + " " + str(u.last_name)
        # set the data in dictionary
        data = {'v_id':vacancy,
            'user_id':id, 'name':name, 'country':u.country, 'city': u.city, 'local_place': u.local_place, 'contact': u.contact,
             'dob':u.date_of_birth, 'profession':cv.profession, 'education':cv.education, 'skills': cv.skills,
              "experience_detail": cv.experience_detail, "reference_name": cv.reference_name, 
              "reference_workat": cv.reference_workat, "reference_position":cv.reference_position, 
              "reference_email": cv.reference_email, "reference_contact": cv.reference_contact
        }
        # render on view_user_detail page with passing some parameter
        return render(request, 'view_user_detail.html',{'cond':'auth','user_name': i.username, 'user_type':user_type, 'data':data })
    else:
        return render(request, 'signin.html')

# function to render contract detail page
def create_contract(request, id = None, vacancy = None):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        user_type = "hod"
        u = User_detail.objects.get(id = id)
        cv = User_CV.objects.get(user = id)
        ud = User_profile.objects.get(user = id)
        v = Vacancy_Detail.objects.get(id = vacancy)
        name = str(ud.first_name) + " " + str(ud.last_name)
        # set data in dictionary
        data = { 'position': v.job_title, 'contract_time': v.contract_time, 'salary': v.range_of_salary,
         'name':name, 'email' : u.email
        }
        # render on add_contract_detail page 
        return render(request, 'add_contract_detail.html',{'cond':'auth','user_name': i.username, 'user_type':user_type, 'data':data })
    else:
        return render(request, 'signin.html')

# function to show the offer page to the user
def offer_list(request):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        user_type = "public"
        if(i.public is True):
            # get the offers for that user in database
            data = list(Contract_detail.objects.filter(email = i.email))
            new_list = []
            # loops get the offers and set in new list
            for j in data:
                new_list.append({'id':j.pk, 'name':j.name, 'position':j.position, 'contract_time':j.contract_time, 'salary':j.salary})
            # pass the list as parameter and render in offer_list page
            return render(request, 'offer_list.html',{'cond':'auth','user_name': i.username, 'user_type':user_type, 'data':new_list })
    else:
        return render(request, 'signin.html')

# function  to show the candidate of the offer contract with its detail in new page
def get_contract(request, id = None):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        k = Contract_detail.objects.get(id = id)
        user_type = "public"
        # check user is public or not
        if(i.public is True):
            if(k.email == i.email): 
                # exception handeling if profile is not found
                try: 
                    p = User_profile.objects.get(user = i.id)
                    # check the signature is found or not 
                    if(p.signature == ""):
                        return render(request, 'profile.html',{'cond':'auth', 'v': p, 'user_name': i.username, 'user_type': user_type, 'message': 'Add your signature first'})
                    s = '/media/' + str(p.signature)
                    new_list = {'id':k.pk, 'name':k.name, 'position':k.position, 'contract_time':k.contract_time, 'salary':k.salary, 'signature':s}
                    # render the contract page 
                    return render(request, 'contract_page.html',{'cond':'auth','user_name': i.username, 'user_type':user_type, 'data':new_list })
                except:
                    return render(request, 'update_profile.html',{'cond':'auth', 'user_name': i.username, 'user_type': user_type})
    else:
        return render(request, 'signin.html')

# function to save the contract detail
def save_contract(request):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        
    else:
        return render(request, 'signin.html')    
        
# function to render on forget password page
def forget_password_page(request):
    if check_user(request) == True:
        home(request)
    else:
        return render(request, 'forget_password.html')

def go_change_new_password(request):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        user_type = "public"
        if(i.hdo is True):
            user_type = "hod"
        if(i.admin is True):
            user_type = "admin"
        return render(request, 'change_password.html',{'cond':'auth', 'user_name': i.username, 'user_type':user_type})
    else:
        return render(request, 'signin.html')

def change_password(email, new_password, re_password):
    try:
        i = User_detail.objects.get(email = email)
        if new_password is None or re_password is None:
            return 'Password should not be empty'
        elif re_password != new_password:
            return 'Password not match with each other'
        elif( len(new_password)<8 ):
            return 'Password must have more than 8 values'
        elif(re.search("[_@$#!%^&*]", new_password) == None):
            return 'Password is not so strong'
        else: 
            set_password = make_password(new_password)
            i.password = set_password
            i.save()
            return True
    except:
        return False    

def check_token(email, token):
    try:
        i = OTP_token.objects.get(email = email)
        db_tok = i.token
    
        if db_tok == token:
            i.delete()
            return  True
        else:
            return "Token not match"
    except:
        return Response("Email not found")
 
def go_to_user_detail(request):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        if i.admin is True:
            user_type = "admin"
            user_list = User_detail.objects.all()
            new_user_list=[]
            for j in user_list:
                if j.admin is False:
                    new_user_list.append(j)

            print(new_user_list)
            return render(request, 'users.html',{'cond':'auth', 'data':new_user_list, 'user_type':user_type})
            return render(request)
        else:
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

def go_to_contract_search(request):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        if i.admin is True:
            user_type = "admin"
            return render(request, 'search_contract.html',{'cond':'auth','user_type':user_type})
        else:
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

def contract_page_detail(request):
    if request.method == 'POST':
        if check_user(request) == True:
            i = User_detail.objects.get(email = request.session['digita'])
            if i.admin is True:
                user_type = "admin"
                try:
                    contract_id = request.POST.get('contract_id')
                    detail = Contract_detail.objects.get(pk = contract_id)
                    data = {'id':detail.pk, 'name':detail.name, 'email':detail.email,'position':detail.position,'contract_time':detail.contract_time,'salary':detail.salary, 'signature_bool':detail.signature_bool}
                    return render(request, 'update_contract.html',{'cond':'auth','user_type':user_type, 'data':data})
                except:
                    messages.error(request, 'Not found')
                    return render(request, 'search_contract.html',{'cond':'auth','user_type':user_type,'msg':"Not found contract id", 'id':contract_id})
            else:
                return render(request, 'signin.html')
        else:
            return render(request, 'signin.html')

def change_user_type(request, id=None):
    if check_user(request) == True:
        i = User_detail.objects.get(email = request.session['digita'])
        if i.admin is True:
            if id is None:
                messages.error(request, 'Not found id. Server error')
                return render(request, 'admin_page.html',{'cond':'auth','user_type':user_type})
            else:
                user_type = "admin"
                i = User_detail.objects.get(pk = id)
                if i.hdo is True:
                    i.hdo = False
                    i.public = True
                elif i.public is True:
                    i.hdo = True
                    i.public = False  
                i.save()                     
                user_list = User_detail.objects.all()
                new_user_list=[]
                for j in user_list:
                    if j.admin is False:
                        new_user_list.append(j)
                return render(request, 'users.html',{'cond':'auth', 'data':new_user_list, 'user_type':user_type})
        else:
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')