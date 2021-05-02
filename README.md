# airticket

## Introduction

Our group developed an online flight reservation system, which mimics the ticket booking system
in the real world such as Priceline. The system cantains both user interface and manager
interface. As a manager, it is easy to use the system to add new airlines and new tickets. As a
passenger, you can search for the flights basing on departure/arrival city and time. The system
provides convenience for travelers to compare tickets from different airlines with different price,
and book whatever you like! We combine the Amazon SES service with our register part so that
when users register they can receice welcome email from us. Also, there is a background process
which releases the manager from manually adding and deleting the flights from database
everyday. It automatically runs once a day to delete old flights and add up-to-date flights with
default parameters.

## User Guide

### Our Website

Online Ticket Reservation System

URL: https://lvprrym0x4.execute-api.us-east-1.amazonaws.com/dev

### As a Manager

1. Enter the URL to go to the homepage of our website, and click **Admin System** to log in as a
    manager. The default admin account is:

```
username: admin
password: 123456
```

```
sign in page for admin
```
```
permission management
```
2. **Permission management** : Add new admin account by setting an username and password
    and submit. The new manager account will be listed above.
3. **Airline management** : Add new airline by filling in the IATA code and callsign of an
    airline/company, and the new airline will be listed above. Notice: You can only choose from
    the aviliable airlines when adding flight, therefore, it is necessary to add at least one airline
    before adding flights.


```
adding flights
```
```
adding airlines
```
4. **Adding new flight** : Add new flight once a time by completing the form, and the new flight
    will be saved in the system for travelers to search and book.


```
order management
```
5. **Order management** : The manager is able to view all the orders, and read the passenger
    information and delete the order.

### As a Passenger

1. **Ticket Searching** : A passenger can use the flight searching function on the homepage of
    our website Search for a satisfying flight by choosing the departure and arrival city and
    departure date and click search.


```
homepage
```
```
search result
```
2. **Ticket Booking** : After clicking search, the passenger will be redirected to a new page of
    results. If there are avilable tickets, it will be shown in the result table. It is easy to make a
    reservation by clicking book.
3. **Log in/Register** : After clicking book, the passenger will be redirected to the log in page.
    He/She can choose to log in or register. Of course, if he/she has already logged in, he/she
    will jump directly to the order confirmation page.If you are first time to register you will
    receive our welcome email.


```
log in page
```
register page


```
welcome email
```
```
order confirmation
```
4. **Order Confirmation** : If a logged-in passenger clicked book button, he/she will be redirected
    to the order confirmation page. In this page, some information is automatically filled in by
    system, and the passenger must provide avilable email address and ID to make the
    reservation.
5. **Personal Center** : After confirmming the order, the passenger will be redirected to his/her
    personal center, where all his/her reservations are shown. He/She can also edit personal
    information in the personal center.


```
my reservation page
```
```
personal information page
```
## Architecture

### File Scheme


### Application Architecture

```
----airticket\ #project name
|----airplane.py #run the application
|----app\
| |----__init__.py
| |----config.py
| |----forms\ #data for building the interface
| | |----auth.py
| | |----search_order.py
| | |----admin.py
| | |----base.py
| |----web\ #main functions for passengers
| | |----auth.py
| | |----search_order.py
| | |----__init__.py
| | |----main.py
| |----admin\ #main function for managers
| | |----auth.py
| | |----__init__.py
| | |----ticket_manage.py
| | |----main.py
| |----static\ #static files
| |----templates\ #html files
| | |----web\
| | |----admin\
| |----data\ #database interaction
| | |----ticket.py
| | |----order.py
| | |----admin.py
```

```
general architecture
```
The graph above is the general architecture of our project with functions of AWS. The code is
deployed to **Lambda** using Zappa, which automatically upload the code to **S3** first. The static files
are also in S3 bucket for Lambda to call. Users use the URL given by **API Gateway** to interact with
the web application. Data is saved in **Dynamodb** , and we use **SES** to send email to users. Also,
the **background process** is deployed seperately in another Lambda function, which interacts
with Dynamodb to update the data. It is set to run once a day by **Cloudwatch**.

### Program Architecture

**administrator**


**user**


## Cost Model

**Assumptions**

1. Each passenger will follow the process: search - book - log in - confirm exactly once when
    they need to make a reservation.
2. Each registered passenger will successfully make a reservation once in six months, and
    search for flights for another five times (although they didn't make a reservation).


3. Since the system works well with the help of background process, the manager will log in to
    admin system once a day to moniter (but do nothing), and add new flights/airlines once a
    week.
4. There are no credits and free quota has been used up.
5. All prices are calculated in USD.

**Basic Model**

**Lambda**

```
Settings:
We use 128 MB memory for both lambda functions. Duration of all requests is
1000ms(calculated by referring to cloudwatch).
Pricing :
Requests : $0.20 per 1M requests
Duration : $0.000000208 per 100ms
Model :
Main function
The number of requests for a passenger in 6 months is:
The number of requests for a manager in 6 months is:
Therefore, the price for requests when there are 10 users is:
```
```
The price for requests when there are 1000 users is:
```
```
The price for requests when there are 1000000 users is:
```
```
The price for duration when there are 10 users is:
```
```
The price for duration when there are 1000 users is:
```
```
The price for duration when there are 1000000 users is:
```
```
Background process
The background process has two functions which can be executed in 100ms, therefore, the
price in 6 months is:
```
**Dynamodb**

```
Settings:
We choose to be charged for on-demand capacity, and only use the core feature (write
request and read request).
```

```
Pricing :
Write request units : $1.25 per million
Read request units : $0.25 per million
Model :
The database is written when passenger register, book a ticket, and adding new
airlines/flights, and is read when passenger log in, search and managers manage the orders.
Therefore, the price for write request per passenger in 6 months is:
```
```
The price for write request for manager and background process in 6 month is:
```
```
The price for read request per passenger in 6 months is:
```
```
The price for read request for manager and background process in 6 month is:
```
```
Thus, when there are 10 users, the price is:
```
```
When there are 1000 users, the price is:
```
```
When there are 1000000 users, the price is:
```
#### S

```
Settings:
The data that is called frequently is less than 1GB.
Pricing:
First 50TB per month: 0.023/GB
Model:
The price in 6 months is:
```
**API Gateway**

```
Settings:
We use HTTP APIs, and the request is cauculated in Lambda part.
Pricing:
First 300 million requests per month: $1 per million
300+ million: $0.9 per million
Model:
The number of requests for a passenger in 6 months is:
The number of requests for a manager in 6 months is:
Therefore, when there are 10 users, the price is:
```

```
When there are 1000 users, the price is:
When there are 1000000 users, the price is:
```
**AWS SES**

```
Pricing: 0.10 for every 1,000 emails
you send after that amount.
Model: Therefore, when there are 10 users, the price is: $
When there are 1000 users, the price is: $
When there are 1000000 users, the price is:
```
**Cloudwatch**

None

**Final Result**

```
10 users:
```
```
1000 users:
```
```
1000000 users:
```
@ Copyright 2019, Nianchong Wu(1005851375) & Jingwen Zhang(1006424040) & Yiyun
Xu(1005678036). Created using Markdown
