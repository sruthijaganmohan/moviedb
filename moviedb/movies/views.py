from django.shortcuts import render
from django.http import JsonResponse
import omdb

# Create your views here.
def ask_omdb(searchItem):
    omdb.set_default('apikey', '134c4e2a')
    movies = omdb.search(searchItem)
    if movies:
        movie_info = ""
        for movie in movies:
            title = movie['title']
            year = movie['year']
            poster_url = movie['poster']
            movie_info += f"Title: {title} Year: {year}<br>"
            movie_info += f'<img src="{poster_url}" alt="{title} Poster"><br>'
        return movie_info
    else:
        return "No movies found"

    
def movies(request):
    if request.method == 'POST':
        searchItem = request.POST.get('searchItem')
        response = ask_omdb(searchItem)
        return JsonResponse({'response': response})
    return render(request, 'movies.html')