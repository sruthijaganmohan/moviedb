from django.shortcuts import render
from django.http import JsonResponse
import omdb

# Create your views here.
def ask_omdb(searchItem):
    omdb.set_default('apikey', '134c4e2a')
    movies = omdb.search(searchItem)
    if movies:
        ans = ""
        for movie in movies:
            title = movie['title']
            year = movie['year']
            poster_url = movie['poster']
            ans += f"Title: {title} Year: {year}<br>"
            ans += f'<img src="{poster_url}" alt="{title} Poster"><br>'
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