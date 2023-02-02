from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from . import util


def index(request):
    entriesToShow = util.list_entries()
    searchFlag = False
    
    if request.method == "POST":
        # Get the user query and check if we have a document that matches
        userQuery = request.POST["q"]
        if util.get_entry(userQuery):
            # Redirect to document page
            return HttpResponseRedirect(reverse("article", kwargs={'title':userQuery}))
        else:
            searchFlag = True
            for entry in entriesToShow.copy():
                if userQuery.lower() in entry.lower():
                    pass
                else:
                    entriesToShow.remove(entry)
        
    return render(request, "encyclopedia/index.html", {
            "entries": entriesToShow,
            "search": searchFlag
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
    

