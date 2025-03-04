from django.db import models


class FlowFile(models.Model):

    FLOW_STATUS_CHOICES = [
        ('processed', 'Processed'),
        ('processing', 'Processing'),
        ('failed', 'Failed'),
    ]

    filename = models.CharField(max_length=50, unique=False)
    status = models.CharField(max_length=20, choices=FLOW_STATUS_CHOICES, default='processing')
    content = models.TextField()
    imported_at = models.DateTimeField(auto_now_add=True)


class MPAN(models.Model):
    # Note: status choices are mapped to a more readable format
    MPAN_STATUS_CHOICES = [
        ('F', 'Failed'),
        ('U', 'Unvalidated'),
        ('V', 'Validated'),
    ]

    mpan_core = models.CharField(max_length=13, unique=True)
    status = models.CharField(max_length=1, choices=MPAN_STATUS_CHOICES, default='F')


class MeterReader(models.Model):
    # TODO: extend with other reading types, for this exercise we will use only the one in the example files
    # Note: status choices are mapped to a more readable format
    READING_TYPES = [
        ('C', 'Customer own read'),
        ('D', 'Deemed or Estimated'),
    ]
    mpan = models.ForeignKey(MPAN, on_delete=models.CASCADE)
    meter_point_id = models.CharField(max_length=10, unique=True)  # J0004 Meter Id (Serial Number)
    meter_type = models.CharField(max_length=1, choices=READING_TYPES, default='C')  # J0171 Reading Type


class Reading(models.Model):
    # Note: status choices are mapped to a more readable format
    READING_METHOD = [
        ('N', 'Not viewed by an Agent or non site visit'),
        ('P', 'Viewed by an Agent or site visit'),
    ]

    READING_FLAG = [
        ('T', 'Valid'),
        ('N', 'Suspect')
    ]

    # Note: optional fields are not used in this exercise, so we skip them for now
    meter_reader_id = models.ForeignKey(MeterReader, on_delete=models.CASCADE)
    meter_register_id = models.CharField(max_length=2)  # J0010 Meter Register ID #register
    reading_date = models.DateTimeField()  # J0016 Reading Date & Time #timestamp
    reading_value = models.DecimalField(max_digits=10, decimal_places=1)  # J0040 Register Reading Value
    reading_flag = models.CharField(max_length=1, choices=READING_FLAG, default='T')  # J0044 Meter Reading Flag
    reading_method = models.CharField(max_length=1, choices=READING_METHOD)  # J1888 Reading Method
    filename = models.ForeignKey(FlowFile, on_delete=models.CASCADE)
