from django.shortcuts import render
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title): 
    entry = util.get_entry(title)

    # Check if the entry exists
    if entry:
        return render(request, "encyclopedia/article.html", {
            "title": title,
            "content": markdown2.markdown(entry)
        })
    else:
        return render(request, "encyclopedia/404.html")
    

