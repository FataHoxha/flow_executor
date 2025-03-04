import os

from django.core.management.base import BaseCommand

from flow_processor import settings
from processor_app.file_parser import process_d0010_file


class Command(BaseCommand):
    help = 'Process D0010 flow files into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path of the file to process')

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, kwargs['file_path'])
        try:
            self.stdout.write(self.style.SUCCESS(f'Processing file: {file_path}'))
            lines = process_d0010_file(file_path)
            self.stdout.write(self.style.SUCCESS(f'Processed {lines} lines'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error processing file: {e}'))
