# Python Application Engineer Interview Task

1. Place 'sales_data.csv' into the project structure inside app directory

2. Position working directory in parent of app directory and run commands

3. Create python virtual environment:

  python -m venv venv

4. Activate the python virtual environment:

  source ./venv/Scripts/activate

5. Install the requirements:

  pip install -r requirements.txt

6. Start the server with command:

  uvicorn app.main:app --reload

7. Make POST /summary request using Postman or some other tool/library
