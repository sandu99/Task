#Python Application Engineer Interview Task

Place 'sales_data.csv' into the project structure inside app directory

Position working directory in parent of app directory and run commands

Create python virtual environment:

python -m venv venv

Activate the python virtual environment:

source ./venv/Scripts/activate

Install the requirements:

pip install -r requirements.txt

Start the server with command:

uvicorn app.main:app --reload

Make POST /summary request using Postman or some other tool/library
