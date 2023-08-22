from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from . import util
import markdown as md
import random as rand



def index(request):
    entries = util.list_entries()
    entries = [entry for entry in entries if entry]

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })


def markdown(value):
    return md.markdown(value, extensions=["markdown.extensions.fenced_code"])


def entry(request, entry):
    entry_value = entry
    markdown_entry = util.get_entry(entry)

    if markdown_entry is None:
        return render(request, "encyclopedia/apology.html")

    body = markdown(markdown_entry)

    return render(request, "encyclopedia/entry.html", {
        "title": entry_value,
        "content": body
    })


def search(request):
    q = request.GET.get('q')
    search_entry = util.get_entry(q)

    entries = util.list_entries()

    matchers = [q]
    matching = {entry: entry for entry in entries if any(xs in entry for xs in matchers)}
    NA = "Sorry, there are no matching results to your search."

    if not matching:
        return render(request, "encyclopedia/search.html", {
            "querie": q,
            "no_match": NA,
        })
    elif search_entry is None:
        return render(request, "encyclopedia/search.html", {
            "querie": q,
            "results": matching,
        })
    else:
        body = markdown(search_entry)

        return render(request, "encyclopedia/entry.html", {
            "title": q,
            "content": body
        })


@csrf_protect
def new_page(request):
    if request.method == "POST":
        new_title = request.POST.get('new_title')
        new_body = request.POST.get('new_body')
        markdown_content = f"# {new_title}\n\n{new_body}"

        current_titles = util.list_entries()

        if new_title in current_titles:
            return render(request, "encyclopedia/apology_create.html", {
                "title": new_title
            })

        else:
            util.save_entry(new_title, markdown_content)
            body = markdown(markdown_content)

            return render(request, "encyclopedia/entry.html", {
                "title": new_title,
                "content": body
            })

    return render(request, "encyclopedia/new_page.html")



def edit_entry(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        edit_entry = util.get_entry(title)

        # Remove the first header from the content
        lines = edit_entry.split('\n')
        without_header = []
        header_removed = False

        for line in lines:
            if line.startswith('#') and not header_removed:
                header_removed = True
            else:
                without_header.append(line)

        edit_entry_without_header = '\n'.join(without_header)

        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "body": edit_entry_without_header
        })

    elif request.method == 'POST':
        new_title = request.POST['title']
        new_body = request.POST['edit_body']

        markdown_content = f"# {new_title}\n\n{new_body}"

        util.save_entry(new_title, markdown_content)

        return redirect('entry', new_title)


def random(request):
    all_entries = util.list_entries()
    random_entry = rand.choice(all_entries)
    body = markdown(util.get_entry(random_entry))

    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": body
    })