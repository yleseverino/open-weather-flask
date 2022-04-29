# openWeatherFlask 🐍

A wrapper for the Open Weather API that returns a city's temperature


## Geting stated
1. Fetch from repo:
    ```bash
    git clone https://github.com/yleseverino/open-weather-flask.git
    ```
2. Change to PythonBuddy directory
    ```bash
    cd open-weather-flask
    ```
3. Create virtualenv based on your own system:
    ```bash
    python3 -m venv venv
    ```
4. Activate virtual environment:
    ```bash
    source venv/bin/activate
    ```
5. Enusre that your virtualenv uses Python 3.10 or a greater version via this command:
    ```bash
    python --version
    ```
    If you don't use a **Python version 3.10** or greater the project will **not work**, because I use in my code the pattern matching, whith is a feature that started in python 3.10
  
6. Pipe requirements to venv folder:
    ```
    pip install -r requirements.txt
    ```
7. Take a look in the .env.example file and create your .env file
    ```bash
    cat .env.example > .env
    ```
    It will be need to set the OPEN_WEATHER_API_KEY with an api key of the [Open Weather API current weather data service](https://openweathermap.org/current). It's free just need to register in the site.
8. Run flask app:
    ```bash
    flask run
    ```
    Open your browser to [localhost:5000](http://localhost:5000) . Voila! 🎉

## How to run the tests

1. To run the test first you need to install the test dependencies inside the venv
    ```
    pip install -r requirements_tests.txt
    ```
2. Finaly just need to run this command in the root dir and the tests will be executed
    ```bash
    pytest
    ```
3. To get the coverage report you need to run this comand
    ```bash
    pytest --cov-report html --cov=openWeatherFlask test/   
    ```
    To look the report just need to open the index.html page inside htmlcov directory