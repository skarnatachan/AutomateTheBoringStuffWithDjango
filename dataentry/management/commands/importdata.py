import csv
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import DataError


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

        # Compare csv header with model's field names
        # get all the field names of the model that we found
        model_fields = [field.name for field in model._meta.fields if field.name != "id"]
        print("model_fields : ", model_fields)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            print("reader : ", reader)
            csv_header = reader.fieldnames
            print("csv_header : ", csv_header)

            # Compare CSV header with model's field names
            if csv_header != model_fields:
                raise DataError(f"CSV file does not match with the {model_name} table fields.")
            for row in reader:
                print("row : ", row)
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data inserted successfully"))
