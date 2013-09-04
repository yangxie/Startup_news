from django.contrib.auth import authenticate, login, logout                                                                                                                   
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.forms import forms                                                                                                                                    
from django.contrib.auth.forms import UserCreationForm                                                                                                                         
from django.contrib.auth.models import User                                                                                                                                  
from django.contrib import auth                                                                                                                                                
from django.http import HttpResponseRedirect, HttpResponse                                                                                                                     
from django.template import RequestContext          

def index_view(request):                                                                                                                                                                return render(request, 'core/base.html') 
