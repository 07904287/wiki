from django.shortcuts import render
import markdown2
from . import util
from django.http import HttpResponse
from django import forms
from django.http import HttpResponseRedirect
import random
import re
from django.contrib import messages
from django.core.files.storage import default_storage


class NewTaskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Entry'}))

class EditTaskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Entry'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if util.get_entry(title):

        return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(title)),
        "title":title
        })
    
    else:
         return render(request, "encyclopedia/404.html", {
        
        })

def error(request):
    return render(request, "encyclopedia/404.html", { 
    })

def create(request):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["description"]
            filename = f"entries/{title}.md"
            if default_storage.exists(filename):
                messages.add_message(request, messages.ERROR, 'Failure to add Entry. Reason: Entry already exists.')
            else:
                util.save_entry(title,entry)
                return HttpResponseRedirect(f"/wiki/{title}")
        
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
                "form": NewTaskForm()
            })


def edit(request, title):
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = EditTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["description"]
            util.save_entry(title,entry)
            return HttpResponseRedirect(f"/wiki/{title}")
        
    else:
        description=util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
                "form": EditTaskForm(initial={'title': title, 'description':description}),
            "title":title,
            })


def get_random(request):
    title = random.choice((util.list_entries()))
    return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(title)),
            "title": title
            })


def search(request):
    query = request.GET['q']
    retVal = util.search_entry(query)
    if isinstance(retVal, str):
        return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(retVal),
        "title":query
        })
    elif isinstance(retVal, list):
        return render(request, "encyclopedia/index.html", {
        "entries": util.search_entry(query)
    })    
    else: 
        raise TypeError