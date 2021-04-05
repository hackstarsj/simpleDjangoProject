"""simpleDjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls.static import static
from simpleFirstApp import views, apiViews
from simpleDjangoProject import settings
from simpleFirstApp.ViewClassForm import ViewClassForm

urlpatterns = [

    # Simple Text Page
    path('', views.IndexPageController, name="index_page"),
    path('firstPage',views.FirstPageController,name="first_page"),

    #loading Html File Pages
    path('htmlPages',views.HtmlPageController,name='html_page'),

    #passing data to html templates
    path('htmlPagesWithData',views.HtmlPageControllerWithData,name='html_page_data'),


    #passing data from url to controller
    path('htmlWithDataPass/<str:url_data>', views.PassingDatatoController, name='html_data_pass'),

    path('addData',views.addData,name="add_data"),

    path('add_student',views.add_student,name="add_student"),

    path('add_teacher', views.add_teacher, name="add_teacher"),

    path('show_all_data', views.show_all_data, name="show_all_data"),

    path('update_student/<str:student_id>',views.update_student,name="update_student"),

    path('edit_student', views.edit_student, name="edit_student"),

    path('delete_student/<str:student_id>', views.delete_student, name="delete_student"),

    path('register_user/',views.RegisterUser,name="register_user"),

    path('login_user/', views.LoginUser, name="login_user"),

    path('save_user',views.SaveUser,name="save_user"),

    path('do_loginn_user',views.DoLoginUser,name="do_login_user"),

    path('homePage/',views.HomePage,name="homepage"),

    path('logout/',views.LogoutUser,name="logout"),

    path('admin/', admin.site.urls),

    path('teststudent',views.testStudent,name='test_student'),

    path('getSubjects',apiViews.getSubjects,name='subjects'),

    path('send_mail_plain',views.SendPlainEmail,name='plain_email'),

    path('send_mail_plain_with_stored_file', views.send_mail_plain_with_stored_file, name='plain_email'),

    path('send_mail_plain_with_file', views.send_mail_plain_with_file, name='plain_email'),

    path('set_session',views.setSession,name='set_session'),

    path('view_session', views.view_session, name='view_session'),

    path('del_session', views.del_session, name='del_session'),

    path('getpdfPage',views.getPdfPage,name='getpdfpage'),

    path('savestudent', apiViews.savestudent, name='savestudent'),

    path('chat/',include('simpleFirstApp.urls')),
    path('viewclassform', ViewClassForm.as_view(), name='viewform'),
    path('multistepformexample', views.multistepformexample, name='multistepformexample'),
    path('multistepformexample_save', views.multistepformexample_save, name='multistepformexample_save'),
    path("multipleupload",views.multipleUpload),
    path("multipleupload_save",views.multipleupload_save),
    path("login_firebase", views.login_firebase),
    path("firebase_login_save", views.firebase_login_save),
    path("ajax_file_upload",views.ajax_file_upload),
    path("ajax_file_upload_save",views.ajax_file_upload_save),

    # NEW ROUTES FOR DIFFERENT TYPES OF VIEWS
    
    #TEMPLATE BASED VIEW
    path("template_view_example",views.TemplateViewExample.as_view(),name="template_view_example"),

    #CLASS BASED VIEW
    path("class_view_example",views.ClassBasedViewExample.as_view(),name="class_view"),

    #LIST VIEW EXAMPLE
    path("list_view_example",views.ListBasedViewExample.as_view(),name="listview_example"),
    path("list_view_example_2",views.ListBasedViewExample2.as_view(),name="listview_example_2"),
    
    #DETAIL BASED VIEW EXAMPLE
    path("course_detail/<slug:pk>",views.DetailsBasedViewExample.as_view(),name="detail_view"),
    path("student_detail/<slug:pk>",views.DetailsBasedViewExample2.as_view(),name="detail_view2"),

    #CREATE VIEW EXAMPLE
    path("create_view_example",views.CreateViewExample.as_view(),name="create_view"),
    path("create_view_example_student",views.CreateViewExample2.as_view(),name="create_view_2"),

    #UPDATE VIEW EXAMPLE
    path("update_course/<slug:pk>",views.UpdateViewExample.as_view(),name="update_view")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
