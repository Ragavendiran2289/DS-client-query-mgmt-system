PROJECT : DS Client Query Management System.

Domain used : SQL / Data Engineering / Python
libraries used  : phython, streamlit, mathplot/altair, my sql connector, pandas, hashlib

Introduction:

Client Query Management System is a streamlined solution designed to efficiently organize, track, and resolve customer support queries. It centralizes all client interactions, ensuring timely responses and improved service quality. By automating query handling and offering real-time status updates, the system enhances productivity and customer satisfaction.

Objective:

The objective of the Client Query Management System is to design and implement an integrated platform that streamlines the submission, tracking, and resolution of client queries. By leveraging a CSV-based initial dataset, MySQL storage, and an interactive Streamlit dashboard, the system aims to improve communication between clients and support teams, enhance query resolution efficiency, and provide actionable insights through real-time performance and workload monitoring.

Projet working:

 The project user interface is created using stream lit.

 The first page which is displayed to the user is the login page. where the user can provide their username, password and select the role to proceed ahead.

The login button will check if the provided user name and password is matching the existing username and password in the database 

The page redirection is done with st.switch_page() function.

The login page uses 5 logic statements.
1. if the register button is clicked the user is redirected to registration page
2. if the entered username and password is not found in the database it will display an error.
3. if the username and password is correct and the selected role is client. The user is redirectd to client query creation page.
4. if the username and password is correct and the selected role is support. the user is redirected to query dashboard.
5. if incorrect role is selected an error is displayed.

The registration page :

This page is primarily used to capture the user information. 
The feilds used are : username, name , email address,  phone number , password and the role. 

To add security for the password we use hashlib
hashlib.sha256(password.encode()).hexdigest()

We are creating the connection to the database with 
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="&***",
        database="***"
    )

after providing the above information they click on submit. 
when the submit button is clicked it will check if any of the fields are missing and prompt the user to fill that information.
If all the feilds are provided it will make a dictionary and inject the information into the database.

query = """
                    INSERT INTO user (username, email, name, phone_number, hashed_password, role)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (username, email, name, number, hashed_pw, role)
                cursor.execute(query, values)
                mydb.commit()
The above code is used to write the information into the table.

After the registration, the user can login to the respective role.

If the user is a client they are redirected to client query page.

Here, the user will provide their email address, mobile number, query title and description and submit the query.

The client function is to raise the query.

If the user is a support they are redirected to support dashboard.

The support dashboard displays all the queries which have been created. irrespactive of the status of the query.

The user can filter the query using the status of the query.

if the query is open the user can close the query.


query filtering:

query = "SELECT * FROM queries WHERE 1=1"
    params = []

    if status_filter and status_filter != "All":
        query += " AND state = %s"
        params.append(status_filter)

Query status udpate: 
 
 sql = """
        UPDATE queries
        SET state = 'Closed',
            closed_on = %s
        WHERE query_id = %s
    """

    values = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query_id)

In the support dashboard, more insight is provided for the management by providing the analysis and data visualisation using  bar chart, area chart and pie chart

In this project we are visualising only the number of queries created per day. How many queries are closed and opened vs closed queries.


Conclusion: This project provides and highlights the basic functionality of a query management system with data visualization feature.
However, this can be further enchanced by adding more categories to the query and providing a client dashboard to view the query created by the particular user.




