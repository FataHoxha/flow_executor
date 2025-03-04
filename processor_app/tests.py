from django.core.management import call_command
from django.test import TestCase
from io import StringIO
from unittest.mock import patch

from processor_app.file_parser import process_d0010_file
from processor_app.models import Reading, FlowFile, MPAN


class ProcessorAppTest(TestCase):
    # Note: in this test, the same file which was provided as example for this exercise, will be used as input.
    # This should be replaced by test files or snippets which are part of a more comprehensive test suite
    INPUT_FILE_PATH = 'processor_app/input_file/DTC5259515123502080915D0010.uff'
    INVALID_FILE_PATH = 'processor_app/input_file/invalid_DTC5259515123502080915D0010.uff'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_file_parser(self):
        # Using the file parser to process the file
        process_d0010_file(self.INPUT_FILE_PATH)

        # Check the number of records created in the Reading model
        reading_obj_count = Reading.objects.all().count()
        flow_file_obj_count = FlowFile.objects.all().count()
        mpan_obj_count = MPAN.objects.all().count()

        # Assert that the number of records matches what was expected
        self.assertEqual(flow_file_obj_count, 1)
        self.assertEqual(mpan_obj_count, 11)
        self.assertEqual(reading_obj_count, 13)

        # Check the status of the FlowFile is `processed`
        flow_file = FlowFile.objects.get(filename='DTC5259515123502080915D0010.uff')
        self.assertEqual(flow_file.status, 'processed')

    def test_unknown_line_type(self):
        try:
            process_d0010_file(self.INVALID_FILE_PATH)
        except Exception as e:
            # Check that the exception message is as expected
            self.assertIn("Unknown line type", str(e))

        # Check the status of the FlowFile is correctly set to failed
        self.assertEqual(FlowFile.objects.get(filename='invalid_DTC5259515123502080915D0010.uff').status, 'failed')

    @patch('sys.stdout', new_callable=StringIO)
    def test_command_happy_path(self, mock_stdout):
        # Using the management command to process the file
        call_command('process_file', self.INPUT_FILE_PATH)

        # Check the number of records created in the Reading model
        self.assertEqual(Reading.objects.all().count(), 13)
        self.assertEqual(MPAN.objects.all().count(), 11)
        self.assertEqual(FlowFile.objects.all().count(), 1)

        # Check the stdout output
        self.assertIn('Processed 35 lines', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_command_invalid_file(self, mock_stdout):
        # Using an invalid file path to raise an error
        call_command('process_file', 'invalid_file_path')

        # Check the stdout output
        self.assertIn('Error processing file:', mock_stdout.getvalue())
