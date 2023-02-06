from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

import markdown2
import random as rand
from . import util

class EntryForm(forms.Form):
    entry = forms.CharField(label="Title", required=True)
    content = forms.CharField(label="", widget=forms.Textarea, required=True)


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


def new(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            # Check if there is already a file with that name
            if util.get_entry(form.cleaned_data["entry"]):
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": True
                })
            else:
                # Create new entry file
                util.save_entry(form.cleaned_data["entry"], form.cleaned_data["content"])
                return HttpResponseRedirect(reverse("article", kwargs={'title':form.cleaned_data["entry"]}))

    return render(request, "encyclopedia/new.html", {
        "form": EntryForm(),
        "error": False
    })


def edit(request, title):
    entry = util.get_entry(title)

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            # Modify the entry content
            util.save_entry(form.cleaned_data["entry"], form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("article", kwargs={'title':form.cleaned_data["entry"]}))

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EntryForm(initial={"entry":title, "content":entry})
    })


def random(request):
    entries = util.list_entries()
    return HttpResponseRedirect(reverse("article", kwargs={'title':rand.choice(entries)}))
