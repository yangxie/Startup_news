import datetime
import hashlib
import random
import re

from auth.models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def signup(request):
    if request.user.is_authenticated():
        return render_to_response('auth/default.html', {'text': 'Logged in already'}, context_instance=RequestContext(request))
    else:
        if request.method == 'GET':
            request.session.set_test_cookie()
            return render_to_response('auth/signup_email.html', '', context_instance=RequestContext(request))
        else:
            if not request.session.test_cookie_worked():
                return render_to_response('auth/default.html', {'text': 'Please enable cookies'}, context_instance=RequestContext(request))
            else:
                request.session.delete_test_cookie()

            email_input = request.POST['email'].strip(' \t\n\r').lower()
            if email_input == '':
                return render_to_response('auth/default.html', {'text': 'Please enter email'}, context_instance=RequestContext(request))
            else:
                if not validateEmail(email_input):
                    return render_to_response('auth/default.html', {'text': 'Please enter valid email'}, context_instance=RequestContext(request))


                user = User.objects.filter(email__iexact=email_input)
                if user.exists():
                    return render_to_response('auth/default.html', {'text': 'Email exists'}, context_instance=RequestContext(request))
                else:
                    username_temp = 'tltemp_'+email_input
                    username_temp = username_temp[:30]

                    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                    password_temp = hashlib.sha1('tltemp'+salt+username_temp).hexdigest()
                    activation_key = hashlib.sha1(salt+username_temp).hexdigest()[:40]
                    user = User.objects.create_user(username_temp, email_input, password_temp)
                    user.is_active=False
                    try:
                        user.save()
                        userprofile=UserProfile.objects.create(user=user, status='I', code=activation_key)
                        userprofile.save()
                        return render_to_response('auth/default.html', {'text': 'Go to /signup?email='+email_input+'&code='+activation_key}, context_instance=RequestContext(request))
                    except Exception as e:
                        print e
                        request.session.set_test_cookie()
                        return render_to_response('auth/default.html', {'text': 'Sign up failed'}, context_instance=RequestContext(request))

def signup_confirm(request):
    if request.user.is_authenticated():
        return render_to_response('auth/default.html', {'text': 'Logged in already'}, context_instance=RequestContext(request))
    else:
        if request.method == 'GET':
            request.session.set_test_cookie()
            try:
                email = request.GET['email']
                code = request.GET['code'].lower()
                print email
                print code
            except Exception as e:
                print e
                return render_to_response('auth/default.html', {'text': 'Link is invalid'}, context_instance=RequestContext(request))

            try:
                user = User.objects.get(email__iexact=email)
                print user.userprofile.code
                if user.userprofile.code.lower() == code:
                    return render_to_response('auth/signup_confirm.html', {'email': email, 'code': code}, context_instance=RequestContext(request))
                else:
                    return render_to_response('auth/default.html', {'text': 'Code doesnt match'}, context_instance=RequestContext(request))
            except User.DoesNotExist:
                return render_to_response('auth/default.html', {'text': 'Email not exists'}, context_instance=RequestContext(request))
        else:
            if not request.session.test_cookie_worked():
                return render_to_response('auth/default.html', {'text': 'Please enable cookies'}, context_instance=RequestContext(request))
            else:
                request.session.delete_test_cookie()

            email_input = request.POST['email'].strip(' \t\n\r').lower()
            code_input = request.POST['code'].strip(' \t\n\r').lower()
            firstname_input = request.POST['first_name'].strip(' \t\n\r')
            lastname_input = request.POST['last_name'].strip(' \t\n\r')
            password_input = request.POST['password'].strip(' \t\n\r')

            try:
                user = User.objects.get(email__iexact=email_input)
                print user.userprofile.code
                if user.userprofile.code.lower() == code_input:
                    user.first_name = firstname_input
                    user.last_name = lastname_input
                    user.set_password(password_input)
                    user.is_active = True
                    user.userprofile.status = 'A'
                    user.userprofile.save()
                    user.save()
                    return render_to_response('auth/default.html', {'text': 'Signed up successfully!'}, context_instance=RequestContext(request))
                else:
                    return render_to_response('auth/default.html', {'text': 'Code doesnt match'}, context_instance=RequestContext(request))
            except User.DoesNotExist:
                return render_to_response('auth/default.html', {'text': 'Email not exists'}, context_instance=RequestContext(request))

def login_view(request):
    if request.user.is_authenticated():
        return render_to_response('auth/default.html', {'text': 'Logged in already'}, context_instance=RequestContext(request))
    else:
        if request.method == 'GET':
            request.session.set_test_cookie()
            return render_to_response('auth/login.html', '', context_instance=RequestContext(request))
        else:
            if not request.session.test_cookie_worked():
                return render_to_response('auth/default.html', {'text': 'Please enable cookies'}, context_instance=RequestContext(request))
            else:
                request.session.delete_test_cookie()

            email = request.POST['email']
            password = request.POST['password']
            try:
                user = User.objects.get(email__iexact=email)
                username = user.username
                print username
            except User.DoesNotExist:
                return render_to_response('auth/default.html', {'text': 'No such email'}, context_instance=RequestContext(request))
            print password
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render_to_response('auth/default.html', {'text': 'Logged in!'}, context_instance=RequestContext(request))
                else:
                    request.session.set_test_cookie()
                    return render_to_response('auth/default.html', {'text': 'The account is inactive'}, context_instance=RequestContext(request))
            else:
                request.session.set_test_cookie()
                return render_to_response('auth/default.html', {'text': 'Email and password dont match'}, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')
