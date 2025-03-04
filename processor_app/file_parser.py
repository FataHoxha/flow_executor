import logging
from datetime import datetime, timezone
from decimal import Decimal

from processor_app.models import MPAN, MeterReader, Reading, FlowFile


def process_d0010_file(file_path):
    """
    Process the file content for D0010 file type and saves the data to the database
    """
    filename = file_path.split('/')[-1]

    with open(file_path, 'r') as file:
        content = file.read()

        # Skip the first and last lines assuming they are header and footer
        lines = content.splitlines()
        if len(lines) > 1:
            lines = lines[1:-1]
            logging.info(f'Processing {len(lines)} lines from {file_path}')

        else:
            logging.info(f'no line to process for {file_path}')
            lines = []

    flow_file, _ = FlowFile.objects.get_or_create(filename=filename, status='processing', content=content)

    datetime_format = '%Y%m%d%H%M%S'
    # Set the timezone to UTC as those might be british times
    utc_timezone = timezone.utc

    # Initialize the variables to store the current MPAN and Meter Reader,
    # so the readings can be associated to the meter_reader which is associated to the MPAN
    current_mpan = None
    current_meter_reader = None

    for line in lines:
        line = line.strip().split('|')

        if line[0] == '026':
            # MPAN identifier
            logging.info(f'Processing MPAN: {line[1]}')
            mpan_core = line[1]
            status = line[2]
            current_mpan, _ = MPAN.objects.get_or_create(mpan_core=mpan_core, status=status)

        elif line[0] == '028':
            # Meter/Reading types
            logging.info(f'Processing Meter Reading: {line[1]}')
            meter_point_id = line[1]
            meter_type = line[2]

            # Associate the Meter Reader to the current MPAN
            if current_mpan:
                logging.info(f'Creating Meter Reader for MPAN: {current_mpan.mpan_core}')
                current_meter_reader, _ = MeterReader.objects.get_or_create(
                    mpan=current_mpan,
                    meter_point_id=meter_point_id,
                    defaults={'meter_type': meter_type}
                )
            else:
                logging.info('Skipping Meter Reader creation as no MPAN found')

        elif line[0] == '030':
            # Register readings
            logging.info(f'Processing Register Reading: {line[1]}')
            meter_register_id = line[1]
            reading_date = datetime.strptime(line[2], datetime_format).replace(tzinfo=utc_timezone)
            reading_value = Decimal(line[3])  # In ElectraLink documentation this is described an integer
            reading_flag = line[6]
            reading_method = line[7]

            # Associate the reading to the current Meter Reader
            if current_meter_reader:
                logging.info(f'Creating Reading for Meter Reader: {current_meter_reader.meter_point_id}')
                Reading.objects.create(
                    meter_reader_id=current_meter_reader,
                    meter_register_id=meter_register_id,
                    reading_date=reading_date,
                    reading_value=reading_value,
                    reading_flag=reading_flag,
                    reading_method=reading_method,
                    filename=flow_file
                )
        else:
            # Unknown line type
            logging.error(f'Unknown line type: {line[0]}')
            flow_file.status = 'failed'
            flow_file.save()
            raise Exception(f'Unknown line type: {line[0]} ')

    # Update the status of the flow file to processed
    flow_file.status = 'processed'
    flow_file.save()

    logging.info(f'File processed {filename} successfully')

    return len(lines)
