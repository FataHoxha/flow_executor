from django.contrib import admin
from processor_app.models import FlowFile, MPAN, MeterReader, Reading


# Searching readings. Allow searching by MPAN and meter serial nuber.
@admin.register(FlowFile)
class FlowFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'status', 'imported_at')
    search_fields = ['filename']


@admin.register(MPAN)
class MPANAdmin(admin.ModelAdmin):
    search_fields = ['mpan_core']
    list_display = ('mpan_core', 'status')


@admin.register(MeterReader)
class MeterReaderAdmin(admin.ModelAdmin):
    search_fields = ['meter_point_id']
    list_display = ('meter_point_id', 'meter_type', 'mpan')


@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    search_fields = ['meter_register_id']
    list_display = ('meter_register_id', 'reading_value',
                    'reading_flag', 'reading_method', 'filename')
