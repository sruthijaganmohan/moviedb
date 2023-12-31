from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
import omdb
from .models import Acc
from django.contrib.auth.decorators import login_required

# Create your views here.
def ask_omdb(searchItem):
    omdb.set_default('apikey', 'apiKey')
    movies = omdb.search(searchItem)
    if movies:
        ans = ""
        for movie in movies:
            title = movie.get('title', 'N/A')
            year = movie.get('year', 'N/A')
            # plot = movie.get('plot', 'N/A')
            # genre = movie.get('genre', 'N/A')
            # rating = movie.get('imdb_rating', 'N/A')
            poster_url = movie.get('poster', 'N/A')
            poster_url = poster_url if poster_url != 'N/A' else 'https://via.placeholder.com/400'
            ans += f'<img src="{poster_url}" alt="{title} Poster"><br>'
            ans += f"<p>{title}\t{year}</p><br>"
            # ans += f"{genre}\t{rating}<br>"
            # ans += f"{plot}<br>"
            ans += "ducks"
        return list(ans.split("ducks"))[:-1]
    else:
        return "No movies found"


    
def movies(request):
    if request.method == 'POST':
        searchItem = request.POST.get('searchItem')
        response = ask_omdb(searchItem)
        return JsonResponse({'response': response})
    return render(request, 'movies.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                acc = Acc(user=user)
                acc.save()
                auth.login(request, user)
                return redirect('movies')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message':error_message})
        else:
            error_message = 'Password does not match'
            return render(request, 'register.html', {'error_message':error_message})
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('movies')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message':error_message})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('movies')

@login_required
def account(request):   
    if request.method == 'POST':
        response = request.POST.get('watchList')
        acc = Acc.objects.get(user=request.user)
        acc.watch_list += response + '\n'
        acc.save()
        return JsonResponse({'response': 'Watch list updated successfully'})
    acc = Acc.objects.get(user=request.user)
    return render(request, 'account.html', {'watch_list': acc.watch_list}) 