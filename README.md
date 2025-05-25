# Flow Executor

This project is a simple Django application that processes a DTC file of type d0010, extract the information 
related to MPAN, meter reader, readings and store them in a database. 
In addition, the application allows those information to be viewed and searched through the django admin interface.

Developed by: Fatbardha Hoxha for the interview at Kraken.

## Running the Application Locally
General info about the application:
- Python version 3.12.1
- Django version 5.1.6

### Clone the repository
Clone the repository by running the following command:
The instructions below vary depending on the way you have setup git on your machine.
1. `git clone https://github.com/FataHoxha/flow_processor.git`

### Create a virtual environment
Within the repository folder, create a virtual environment, activate it, and install the required packages.
1. Navigate to the project directory 

2. Create the virtual environment: 

   `python -m venv <venv_flow_processor_3.12>`

3. Activate the virtual environment:

   `source <venv_flow_processor_3.12>/bin/activate `

4. Install the packages required:

    `pip install -r requirements.txt`


### Set up the database
Set up the database by running the following commands:
1. `python manage.py migrate`

### Set up the superuser account
Set-up the superuser account so that you can log in the Django admin interface.
1. `python manage.py createsuperuser`
2. Follow the prompts to set up the superuser account by providing a username, email address, and password.

### Import the data from the D0010 file
The example files are located in the processor_app/input_file folder that they can be easily located to test the application.
Import the data from the D0010 file by running the following command:
1.  `python manage.py process_file processor_app/input_file/DTC5259515123502080915D0010.uff`

If the file is processed successfully, you should see the following message:
_"Processed 35 lines"_

### Start the server
Finally run the server which will allow you to view the data in the Django admin interface.
1. python manage.py runserver
2. Access the application by navigating to http://127.0.0.1:8000/admin in the browser of your choice.
3. Log in to the Django admin interface using the superuser account created in the previous step.
4. You should see the following models in the admin interface:
   - Flow Files
   - MPANs
   - Meter readers
   - Readings


### Run the Tests
To run the tests, run the following command:
1. `python manage.py test processor_app`



## Implementation Details
### Design Decisions
The following design decisions were made during the implementation of the application.

The database models were designed to represent the information extracted from the D0010 file in a structured way.
From the reference site, [electralink](https://www.electralink.co.uk/dtc-catalogue/), it is mentioned that the objects are hierarchical: 
with a FlowFile containing multiple MPANs, each MPAN containing multiple MeterReaders,
and each MeterReader containing multiple Readings.
With this in mind, the models were designed to reflect this hierarchy.

Give the example of the file _DTC5259515123502080915D0010.uff_, I've assumed that the file has a small size.
I've excluded the first and last lines of this file, as they most likely are header / footer,
and they didn't seem relevant to this exercise.

### Components
The main components implemented in this exercise are:
- **models.py**: The models are used to define the structure of the database tables. The models used in this application are:
  - FlowFile: Represents the D0010 file that is processed by the application.
  - MPAN: Represents the MPAN information extracted from the D0010 file.
  - MeterReader: Represents the meter reader information extracted from the D0010 file.
  - Reading: Represents the reading information extracted from the D0010 file.
- **file_parser.py**: Handles the processing of the D0010 file and extraction of the information.
- **management/commands/process_file.py**: Custom management command that calls the file_parser.
- **admin.py**: Allows the models to be viewed and searched in the Django admin interface.
- **tests.py**: Contains the tests for the models and the file_parser.



## Space for Improvements
The following points contain some possible improvements that can be made to enhance the project:
- Create data model validations, maybe by using pydantic, so that the data extracted from the D0010 file is correct and complete, even before it is stored in the database.
- Add more validations that checks the status of the file, so that correctly processed files are not processed again.
- Ensure that the application can handle larger file sizes, so that the content is not stored in the database but only a reference to its location.
- Currently the application is only able to process D0010 files, it would be useful to add support for other file types.
- Handle the case where the file is not in the correct format, and provide a meaningful error message to the user.
- Add more tests to cover edge cases and ensure that the application works as expected in all scenarios.
- Instead of using venv and requirements.txt, use poetry to manage the dependencies and the virtual environment.
- Use a more robust database like PostgreSQL for production deployments.
- Create a separate testing folder for the test files, so that the test files are not mixed with the input files.
