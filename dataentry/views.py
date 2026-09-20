from django.core.management import call_command
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import get_all_custom_models
from uploads.models import Upload

def home(request):
    context = {
    }
    return render(request, 'dataentry/home.html', context)

def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')
        print("file_path : ", file_path)
        print("model_name : ", model_name)

        # Store this file inside the upload model
        upload = Upload.objects.create(file=file_path, model_name=model_name)

        # Absolute filesystem path of the stored file
        file_path = upload.file.path
        print("absolute file_path : ", file_path)
        try:
            call_command('importdata', file_path, model_name)
            messages.success(request, 'Successfully imported data')
        except Exception as e:
            messages.error(request, str(e))
        return redirect('import_data')
    else:
        custom_models = get_all_custom_models()
    context = {
        "custom_models": custom_models,
    }
    return render(request, 'dataentry/importdata.html', context)