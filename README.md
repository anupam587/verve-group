# Verve Group Application

This project is a Verve group application that provides endpoints for managing promotions data. It includes functionalities to fetch promotions by ID, upload promotions data from a CSV file, and more.

## Installation

To run this application locally, follow these steps:

1. Clone this repository to your local machine:
   ```bash
   git clone git@github.com:anupam587/verve-group.git
   ```
2. Navigate to the project directory:
   ```bash
   cd verve-group
   ```
3. Install the required Python dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
4. Default App configuration
   ```
   App_host: localhost
   App_port: 1321
   ```
5. Default Mongodb configuration:
   ```
   mongo_host: mongodb || 127.0.0.1 ||
   mongo_username: admin
   mongo_password: password
   mongo_dbname: vervedb
   connection string: mongodb://admin:password@127.0.0.1:27017/?tls=false
   ```
6. Above configuration can be changed in config.json and .env file.

## Running the Application

Once the dependencies are installed, you can run the FastAPI application and MongoDB server using Docker Compose. Ensure Docker is installed and running on your system.

#### first way
1. Build the Docker images:
   ```bash
   docker-compose build
   ```
2. Start the containers:
   ```bash
   docker-compose up
   ```

#### second way
   ```bash
   docker-compose up --build
   ```

Note:
Application server and mongodb will be running in seprate container.


The Application server(FastAPI) will be accessible at http://localhost:1321.

#### Note: 
config.json and .env file contains configuration parameters for running application server
   and mongodb server.


## Application Usage

### Fetch Promotion by ID

To fetch a promotion by its ID, send a GET request to the /promotions/{promotion_id} endpoint. Replace {promotion_id} with the actual ID of the promotion.

Example:
   ```bash
   curl -X GET "http://localhost:1321/promotions/0464518f-848f-4845-af64-5fb45a54ddd0"
   ```
Response:
   ```
   {
    "id": "0464518f-848f-4845-af64-5fb45a54ddd0",
    "price": 62.454782,
    "expiration_date": "2018-07-25 11:56:25 +0200 CEST"
   }
   ```

### Upload Promotions from CSV File

To upload promotions data from a CSV file, send a POST request to the /uploadfile/ endpoint with the CSV file as form data.

Example:
   ```bash
   curl -X POST -F "file=@promotions.csv" "http://localhost:1321/add-promotions/"
   ```
Response:
   ```
   {
    "status": "success",
    "message": "Promotions added successfully"
   }
   ```

Replace promotions.csv with the path to your CSV file.

## Additional Features
### 1. Handling Large CSV files with billion entries
Here are some strategies to handle large csv files:

Streaming or Batch Processing: 
```
Instead of loading the entire CSV file into memory at once, do streaming processing techniques using spark to process the file content in chunks to reduce memory usage.
```

Parallel Processing: 
```
Utilize parallel processing techniques to distribute the workload across multiple CPU cores or machines. This can significantly speed up data processing, especially for CPU-bound tasks.
```

Optimized Database Operations: 
```
Optimize database operations, such as bulk inserts and updates, to minimize the number of database transactions and improve performance.
```

Compression: 
```
Consider compressing the CSV file to reduce its size before processing. This can help reduce disk I/O and network bandwidth requirements, especially for large files.
```

### 2. Peak Period Performance (more than 1M requests/min)
Asynchronous Programming:
``` 
Use asynchronous programming techniques to handle I/O-bound operations asynchronously. This allows the application to perform other tasks while waiting for I/O operations to complete, improving overall throughput.
```

Indexing: 
```
Create appropriate indexes on ID field used for querying data to speed up database queries. This can improve the performance of read operations, especially when fetching data by ID or other criteria.
```

Caching: 
```
Implement caching mechanisms (e.g. Redis, Memcached) to store frequently accessed data in memory, reducing the need for repeated database queries.
```

Data Partitioning: 
```
If possible, partition the data across multiple database servers or shards to distribute the workload and improve scalability.
```

Resource Allocation: 
```
Allocate sufficient resources (CPU, memory, disk) to the application and database servers to ensure optimal performance. Monitor resource usage and scale up or out as needed.
```

### 3. Operate App in Production
#### Deployment:
```
1. Choose a cloud provider or hosting service (e.g., AWS, GCP, Azure) for deploying your application.
2. Use Jenkins to create the CI/CD pipeline 
3. Add few unit test cases (pytest framework) in application to test basic functionality before deploying in cloud.
3. Set up a virtual machine (VM) or containerized environment (e.g., Docker, Kubernetes) to host your application.
3. Deploy Application server on (ec2 or eks instances) and MongoDB server to the chosen environment.
4. Configure network settings, security policies, and firewall rules to ensure proper communication and access control.
```
#### Scaling:
```
1. Monitor the resource usage (CPU, memory, disk I/O) of your application and database servers.
2. Implement horizontal scaling by adding more instances of your application and MongoDB server to handle increased load.
3. Use load balancers and auto-scaling groups to distribute incoming traffic evenly across multiple instances and automatically adjust capacity based on demand.
4. Configure caching mechanisms (e.g., Redis, Memcached) to offload frequently accessed data and reduce database load.
```
#### Monitoring:
```
1. Set up monitoring and alerting systems to track the health and performance of your application and infrastructure.
2. Use tools like Prometheus, Grafana, or Datadog to monitor metrics such as response time, throughput, error rates, and resource utilization.
3. Monitor database performance metrics (e.g., query execution time, read/write throughput, connection pool usage) to identify bottlenecks and optimize database operations.
4. Implement logging and log aggregation to capture and analyze application logs, including errors, warnings, and informational messages.
5. Set up anomaly detection and threshold-based alerts to notify you of any abnormalities or potential issues in real-time.
```