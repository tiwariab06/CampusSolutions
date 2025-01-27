from django.shortcuts import render, redirect, HttpResponse
from FacultyUploads.models import Pyq
import os
from django.shortcuts import get_object_or_404


# Display Pyq's.
def showPyq(request):

    if request.method == "POST":
        sem = request.POST.get("semester")
        session = request.POST.get("session")
        pyq = Pyq.objects.filter(semester=sem, session=session)
        for i in pyq:
            print(i.name)
        return render(request, "showPyq.html", {"pyq": pyq})

    return render(request, "showPyq.html")


# download Pyq's.


def downloadPyq(request, id):
    pyq = get_object_or_404(Pyq, id=id)
    file_path = pyq.url.path  # Get the file path as a string
    file_extension = os.path.splitext(file_path)[1]  # Extract the file extension
    response = HttpResponse(pyq.url, content_type="application/force-download")
    response["Content-Disposition"] = 'attachment; filename="%s%s"' % (
        pyq.name,
        file_extension,
    )
    return response
