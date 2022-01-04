# Car Hire Management System

The main focus of the business is renting cars and vans, and the database is to manage the booking system.  

Table of Contents
=================
  * [Setup](#setup)
  * [Usage](#usage)

## Setup
Fistly, clone this repository:
```
git clone https://github.com/WaelAshraf/CarHireManagementSystem.git
```
API requires:

- Flask 
```bash
pip install flask
```
- Flask Restful
```bash
pip install flask-restful
```
- flask_mysqldb for my sql
```bash
pip install flask_mysqldb
```
 - Flask_CORS
  ```bash
  pip install flask_cors
  ```
  - apscheduler for daily scheduled tasks
 ```bash
  pip install apscheduler
  ```
  - smtplib for mail by gmail
  ```bash
  pip install smtplib
  ```
  
  Database:
  mysql server and workbench through installer: https://dev.mysql.com/downloads/installer/
  
## Usage

### Step 1: Prepare mysql DB
- Create car_hire_managment_system Database then run mysql.sql script in it

### Step 2: Run Flask Server
```
python api.py
```

### Step 3: Use the API Request content type: JSON
- Send post request to http://127.0.0.1:5000/api/customer With "/api/customer/" as end point with the following body tags:
    - "name"
    - "phone"
    - "mail"
    - "vehicle_category"
    - "date_of_hire"
    - "date_of_ret"
    
 - Send get request to http://127.0.0.1:5000/api/customer With "/api/customer/" as end point : to get all customers and Invoices if any
 - Send get request to http://127.0.0.1:5000/api/customer/:id With "/api/customer/:id" as end point : to get customer by id
 - Send delete request to http://127.0.0.1:5000/api/customer/:id With "/api/customer/:id" as end point : to delete customer and its bookings by id
 - Send put request to http://127.0.0.1:5000/api/customer/:id With "/api/customer/:id" as end point : to upate customer info by id with the following body tags:  
    - "name"
    - "phone"
    - "mail"
    
 - Send put request to http://127.0.0.1:5000/api/customer/edit/:id With "/api/customer/:id" as end point : to add vehicle rental booking to existing customer by id with the following body tags:  
    - "vehicle_category"
    - "date_of_hire"
    - "date_of_ret"
  
  **Examples**:

- Ex:
```
Post: 
{
 "name":"wael",
 "phone":"01094401355",
 "mail":"wael.ashraf.anwar@gmail.com",
 "vehicle_category":"family car carry up to 7",
 "date_of_hire":"2022-01-05",
 "date_of_ret":"2022-01-10"	
}
 ```
 - Ex:
```
Put: 
{
 "name":"wael",
 "phone":"01094401355",
 "mail":"wael.ashraf.anwar@gmail.com",
}
 ```
 - Ex:
```
Put: 
{
 "vehicle_category":"family car carry up to 7",
 "date_of_hire":"2022-01-05",
 "date_of_ret":"2022-01-10"	
}
 ```

