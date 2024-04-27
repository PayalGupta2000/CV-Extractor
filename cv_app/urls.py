from django.urls import path
from . import views

urlpatterns = [
    path("",views.upload_cv),
    path("contact_info",views.extract_contact_info),
    path("text-from-pdf",views.extract_text_from_pdf),
    path("process_file",views.process_cv_file),
    path("text-from-doc",views.extract_text_from_doc),
]
