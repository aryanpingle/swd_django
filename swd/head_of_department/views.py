from django.shortcuts import render
from django.http import HttpResponse
from main.models import Student
from django.db.models import Q

def index(request):
    """
    [SINGLE DEGREE ONLY]
    Handles GET and POST requests. Every time the HOD clicks on the search button a POST request will be initiated
    """

    context = {}
    hod_user = request.user
    context.update({ "hod_user": hod_user })

    if not request.POST:
        return render(request, "hod-single_degree.html", context)

    # Must be POST or the like

    data = request.POST

    branch = data["branch"]
    year = data["year"]
    flag__only_single_degree = "checkbox--only-single-degree" in data

    query = None
    if flag__only_single_degree:
        query = Q(bitsId__startswith = f"{year}{branch}")
    else:
        query = Q(bitsId__contains = branch, bitsId__startswith = str(year))

    filtered_students = Student.objects.filter(query).order_by("-cgpa")

    context.update({ "students": filtered_students })

    return render(request, "hod-single_degree.html", context)

def dual_degree(request):
    """
    Handles GET and POST requests. Every time the HOD clicks on the search button a POST request will be initiated
    """

    context = {}
    hod_user = request.user
    context.update({ hod_user: hod_user })

    if request.GET:
        return render(request, "hod-dual_degree.html", context)

    return render(request, "hod-dual_degree.html", context)