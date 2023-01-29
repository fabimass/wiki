from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    
    # Check if the title provided matches with one of the articles (I lowercase each article name to avoid discrepancies)
    if title.lower() in list(map(str.lower, util.list_entries())):
        return render(request, "encyclopedia/article.html", {
            "title": title
        })
    else:
        return render(request, "encyclopedia/404.html")
    

