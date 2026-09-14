from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Employee, Attendance, Salary
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def employee_list(request):

    search = request.GET.get("search", "")

    employees = Employee.objects.all()

    if search:
        employees = employees.filter(name__icontains=search)

    return render(request, "employees/employee_list.html", {
        "employees": employees,
        "search": search
    })


@login_required
def employee_add(request):
    if request.method == "POST":

        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        department = request.POST["department"]
        position = request.POST["position"]
        salary = request.POST["salary"]
        joining_date = request.POST["joining_date"]

        Employee.objects.create(
            name=name,
            email=email,
            phone=phone,
            department=department,
            position=position,
            salary=salary,
            joining_date=joining_date
        )

        return redirect("employee_list")

    return render(request, "employees/employee_add.html")


@login_required
def employee_edit(request, id):

    employee = Employee.objects.get(id=id)

    if request.method == "POST":

        employee.name = request.POST["name"]
        employee.email = request.POST["email"]
        employee.phone = request.POST["phone"]
        employee.department = request.POST["department"]
        employee.position = request.POST["position"]
        employee.salary = request.POST["salary"]
        employee.joining_date = request.POST["joining_date"]

        employee.save()

        return redirect("employee_list")

    return render(request, "employees/employee_edit.html", {
        "employee": employee
    })

@login_required
def employee_delete(request, id):

    employee = Employee.objects.get(id=id)

    employee.delete()

    return redirect("employee_list")

def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next", "dashboard"))

        return render(request, "employees/login.html", {
            "error": "Username or password is incorrect."
        })

    return render(request, "employees/login.html")

def user_logout(request):

    logout(request)

    return redirect("user_login")

@login_required
def dashboard(request):
    total_employees = Employee.objects.count()
    total_departments = Employee.objects.values("department").distinct().count()
    total_salary = Employee.objects.aggregate(Sum("salary"))["salary__sum"] or 0

    return render(request, "employees/dashboard.html", {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "total_salary": total_salary,
    })
@login_required
def attendance_list(request):
    attendances = Attendance.objects.all().order_by("-date")

    return render(request, "employees/attendance_list.html", {
        "attendances": attendances
    })


@login_required
def attendance_add(request):

    employees = Employee.objects.all()

    if request.method == "POST":
        employee_id = request.POST["employee"]
        date = request.POST["date"]
        status = request.POST["status"]

        Attendance.objects.create(
            employee_id=employee_id,
            date=date,
            status=status
        )

        return redirect("attendance_list")

    return render(request, "employees/attendance_add.html", {
        "employees": employees
    })

@login_required
def salary_list(request):
    salaries = Salary.objects.all().select_related("employee")

    return render(request, "employees/salary_list.html", {
        "salaries": salaries
    })

@login_required
def salary_add(request):

    employees = Employee.objects.all()

    if request.method == "POST":

        employee_id = request.POST["employee"]
        month = request.POST["month"]
        basic_salary = request.POST["basic_salary"]
        bonus = request.POST["bonus"]
        deduction = request.POST["deduction"]

        Salary.objects.create(
            employee_id=employee_id,
            month=month,
            basic_salary=basic_salary,
            bonus=bonus,
            deduction=deduction
        )

        return redirect("salary_list")

    return render(request, "employees/salary_add.html", {
        "employees": employees
    })


def employee_api(request):

    employees = Employee.objects.all()

    data = []

    for employee in employees:
        data.append({
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "phone": employee.phone,
            "department": employee.department,
            "position": employee.position,
            "salary": str(employee.salary),
            "joining_date": str(employee.joining_date),
        })

    return JsonResponse(data, safe=False)
