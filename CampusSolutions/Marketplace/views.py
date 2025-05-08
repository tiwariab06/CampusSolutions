# views.py

from django.shortcuts import render, redirect
from .forms import ResourceForm
from .models import Resources
from django.contrib import messages


def upload_resource(request):
    if request.method == "POST":
        # extract and save form data
        Type = request.POST.get("Type")
        subject = request.POST.get("subject")
        semester = request.POST.get("semester")
        Print = request.POST.get("Print")
        Price = request.POST.get("Price")
        Seller_email = request.POST.get("Seller_email")
        Seller_mobile = request.POST.get("Seller_mobile")

        Resources.objects.create(
            Type=Type,
            subject=subject,
            semester=semester,
            Print=Print,
            Price=Price,
            Seller_email=Seller_email,
            Seller_mobile=Seller_mobile,
        )

        messages.success(request, "Resource uploaded successfully!")
        return redirect("upload_resource")  # replace with your URL name

    return render(request, "upload_resource.html")


def show_resources(request):
    resources = Resources.objects.all()
    return render(request, "show_resources.html", {"resources": resources})
