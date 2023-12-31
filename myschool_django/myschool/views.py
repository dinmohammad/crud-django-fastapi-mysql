import base64
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import requests
from django.contrib import messages


from myschool import settings

base_url = settings.BASE_URL


def homePage(request, image_bytes=None):
    api_url = f'{settings.BASE_URL}/all_student/'
    response = requests.get(api_url).json()
    print(response)
    if response is None:
        response = None
    return render(request, 'pages/homepage.html', {'response': response})


def studentDetails(request, std_id):
    api_url = f'{settings.BASE_URL}/get_student/{std_id}'

    # Make an HTTP GET request to the API
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
    else:
        data = {}  # Handle the case where the API request failed

    return render(request, 'pages/studentDetails.html', {'data': data})


def newStudentPage(request):
    return render(request, 'pages/newStudent.html')


def createStudent(request):
    if request.method == 'POST':
        # Get form data from the request
        std_name = request.POST['std-name']
        std_class = request.POST['std-class']
        std_details = request.POST['std-details']
        std_img = request.FILES.get('std_img')

        data = {
            "name": std_name,
            "stdcls": std_class,
            "details": std_details,
            "user_id": 5,
        }
        files = {'file': (std_img.name, std_img.read())}
        # data1 = json.dumps(data)

        print(data)

        api_url = f'{settings.BASE_URL}/create_student/'
        response = requests.post(api_url, data=data, files=files)

        if response.status_code == 201:
            alert_message = "Student record created successfully."
            alert_type = "success"
            messages.success(request, alert_message, alert_type)
            return redirect('/')
        else:
            print("Failed status code:", response.status_code)
            return JsonResponse({"message": "Failed to create a student record. Please try again"}, status=500)

    return render(request, 'pages/homepage.html')


def deleteStudent(request, std_id):
    api_url = f'{settings.BASE_URL}/delete-post/{std_id}'
    response = requests.delete(api_url)

    if response.status_code == 200:
        return redirect('/')
    else:
        return HttpResponse("Failed to drop student", status=500)


def editStudentPage(request, std_id):
    api_url = f'{settings.BASE_URL}/get_student/{std_id}'

    # Make an HTTP GET request to the API
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
    else:
        data = {}  # Handle the case where the API request failed
    return render(request, 'pages/editStudent.html', {'data': data})


def updateStudent(request, std_id):
    if request.method == 'POST':
        # Get form data from the request
        std_name = request.POST['std-name']
        std_class = request.POST['std-class']
        std_details = request.POST['std-details']

        data = {
            "name": std_name,
            "stdcls": std_class,
            "details": std_details,
            "user_id": 5,
        }

        files = {}

        if 'std_img' in request.FILES:
            std_img = request.FILES['std_img']
            # files['file'] = (std_img.name, std_img.read())
            files = {'file': (std_img.name, std_img.read())}

        api_url = f'{settings.BASE_URL}/update-student/{std_id}'
        response = requests.put(api_url, data=data, files=files)

        if response.status_code == 201:  # 201 Created
            return redirect('/')
        else:
            print(f"FastAPI Response: {response.status_code}, {response.content}")
            return HttpResponse("Failed to edit student", status=500)


def aboutPage(request):
    return render(request, 'pages/about.html')
