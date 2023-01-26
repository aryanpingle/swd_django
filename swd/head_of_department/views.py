from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Student, HostelPS, HeadOfDepartment
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """
    [B.E. DEGREE ONLY]
    Handles GET and POST requests. Every time the HOD clicks on the search button a POST request will be initiated
    """

    context = {}
    user = request.user
    is_hod = False if not HeadOfDepartment.objects.filter(user=user) else True
    if (not user.is_superuser) and (not is_hod):
        return redirect("/")

    context.update({ "hod_user": user })

    if not request.POST:
        return render(request, "hod-single_degree.html", context)

    # Must be POST or the like

    data = request.POST

    branch = data["branch"]
    year = data["year"]
    flag__only_single_degree = "checkbox--only-singlites" in data

    query = None
    if flag__only_single_degree:
        query = Q(bitsId__startswith = f"{year}{branch}")
    else:
        # Suppose year = 2020 & branch = A8
        # Then it should match 2020A8 and 2021B*A8
        query = Q(bitsId__startswith = f"{year}{branch}") | Q(bitsId__startswith = f"{int(year) - 1}B", bitsId__contains = branch)

    # Get students and their corresponding hostelPS objects
    filtered_students = Student.objects.filter(query).order_by("-cgpa")
    corresponding_hostelps = HostelPS.objects.filter(student__in = filtered_students).order_by("-student__cgpa")
    # student_data -> ((<student obj>, <hostel_obj>), ...)
    student_data = tuple(zip(filtered_students, corresponding_hostelps))

    context.update({ "student_data": student_data })

    return render(request, "hod-single_degree.html", context)

@login_required
def dual_degree(request):
    """
    Handles GET and POST requests. Every time the HOD clicks on the search button a POST request will be initiated
    """

    context = {}
    user = request.user
    is_hod = False if not HeadOfDepartment.objects.filter(user=user) else True
    if (not user.is_superuser) and (not is_hod):
        return redirect("/")

    context.update({ "hod_user": user })

    if request.GET:
        return render(request, "hod-dual_degree.html", context)

    return render(request, "hod-dual_degree.html", context)