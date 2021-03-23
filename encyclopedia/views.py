from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import Markdown
import random
from . import util
from .forms import EntryForm


md = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    f_entry = util.get_entry(title)
    if f_entry == None:
        return render(request, "encyclopedia/page_not_found.html")
    return render(request, "encyclopedia/title.html", {
        "entrytitle":  title,
        "entrybody": md.convert(f_entry)
    })


def create_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entrytext = form.cleaned_data["entrytext"]
            if title in util.list_entries():
                return render(request, "encyclopedia/entry_already_exists.html")
            else:
                util.save_entry(title, entrytext)
                return HttpResponseRedirect(reverse("entrypage", args=[title]))
    else:
        form = EntryForm()
    return render(request, "encyclopedia/entry_form.html", {
        'form': form
    })


def edit_entry(request, title):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entrytext = form.cleaned_data["entrytext"]
            util.save_entry(title, entrytext)
            return HttpResponseRedirect(reverse("entrypage", args=[title]))
    else:
        form = EntryForm()
        form.fields["title"].initial = title
        form.fields["entrytext"].initial = util.get_entry(title)
    return render(request, "encyclopedia/edit_entry_form.html", {
        'form': form
    })


def random_entry(request):
    selected_entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entrypage", args=[selected_entry]))


def search(request):
    query = request.GET.get("query")
    search_results = [q for q in util.list_entries() if query.lower() in q.lower()]
    if len(search_results) == 1:
        return entry(request, search_results[0])
          
    return render(request, "encyclopedia/search.html",{
        "entries": search_results
    })