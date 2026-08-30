import csv
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

# Proposed command - python manage.py importdata file_path model_name

class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to CSV file")
        parser.add_argument('model_name', type=str, help="Table's name")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        # model_name = kwargs["model_name"].capitalize()
        model_name = kwargs["model_name"]
        # Search for the model across all installed apps
        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
            except LookupError:
                continue   # model not found in this app, continue searching in next app.
        if not model:
            raise CommandError(f"Model {model_name} not found in any app!")

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data inserted successfully"))
