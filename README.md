# Weather API (FastApi Implementation)

## This API provides weather data and statistics via API endpoints. The following are the endpoints:

     - /api/weather - retrieves weather data
     - /api/weather/stats - provides statistics about the data
     - /docs - provides documentation using OpenAPI

## Prerequisites
To use this API, the following prerequisites are required:

    - Python (3.7 or higher)
    - Virtualenv
    - SQLite
    - AWS account (if deploying to AWS)

# Installation and Usage

 ## To install the required dependencies and use this API, follow these steps:

 - Create and activate a virtual environment using    the  following commands:
   
   ``` 
   python -m venv venv 
   ```

# Activate the virtual environment using the following commands:

Windows: venv\Scripts\activate
Linux and Mac: source venv/bin/activate
Install the required dependencies using the following command:

```
pip install -r requirements.txt
````

# Move to the source directory:

``` 
cd src
```

# Ingest the data using the following command:

```
python data_ingestion.py
```

# Run the server using the following command:

```
uvicorn run_app:app --reload
```

# Access the API endpoints using the following URLs:

    - http://127.0.0.1:8000/api/weather/ - for weather records
    - http://127.0.0.1:8000/api/weather/stats - for weather stats
    - http://127.0.0.1:8000/docs - UI specification of API

# Running tests
## To run tests, use the following commands:

 ```
  cd src

  pytest
 ```

# Cloud Deployment Strategy (AWS)
## To deploy the API to AWS, follow these steps:

 - Create a Python project with an app.py file containing the FastAPI application code.

 - Create a new AWS Lambda function and configure its runtime to use Python 3.8 or later.

 - Package your Python code and any dependencies as a ZIP file and upload it to AWS Lambda.

 - Set the handler function in your Lambda function to the name of your FastAPI application function.

 - Create an API Gateway, REST API, or HTTP API that integrates with your Lambda function.

 - Deploy respective APIs to a publicly accessible endpoint.

 - Use RDS to store the ingested data.

# Conclusion
When deploying to AWS, scalability and security features can be easily managed by using strategies like autoscaling and load balancing. Additionally, with AWS's robust security features, developers can ensure that their API is protected against potential security threats.