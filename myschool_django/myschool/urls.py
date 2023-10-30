from django.contrib import admin
from django.urls import path

from myschool import views


urlpatterns = [
    path('', views.homePage),
    path('new-student/', views.newStudentPage),
    path('create-student/', views.createStudent, name="create-student"),
    path('student-details/<int:std_id>', views.studentDetails),
    path('delete-student/<int:std_id>', views.deleteStudent, name="delete-student"),
    path('edit-student/<int:std_id>', views.editStudentPage, name="edit-student"),
    path('update-student/<int:std_id>', views.updateStudent, name="update-student"),
    path('about-us/', views.aboutPage),
    path('admin/', admin.site.urls),
]



