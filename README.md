# Post-Covid Bucket List Budget Planner

Resource:

Link to the Github Project Board: https://github.com/AbbyXSu/Bucket_List_Budgeter/projects/1


Brief:

This documentation detailed all the necessary procedures and actions that were taken to complete this functional web application and fulfilled tests to ensure the app is fully utilise. The objective of this project is to create an functional CRUD application in Python, following best practices and design principles and produce the MVP with utilisation of Python, Pytest, SQL server via AWS RDS, Git (as Version Control),Flask HTML(as front end),CSS and Jenkins(as CI server)in both Linux and Windows system on AWS VM.

Additional specification of the project is as follow:

1. Full ERD and documentation of the design and development of the application.
2. Utilisation of Cloud Hosted managed Relational Database modelling five tables.
3. Unit testing using Pytest.
4. A fully functional front end web application via Flask.
5. Continuous Integration via Jenkins and version control system Git.

Approach of the project:

This project is inspired by one of the most contemporary topic - Covid 19.

As the world is impacted by lockdowns and travel restriction, there are many things people wish to do an yet could not deliver due to the current situation. the web app project aim to explore the solution of helping people to save up during the Lockdown and plan ahead for their post-pandemic life, and it is hoped that in developing and designing this web app, it will encourage people to look at the positive side during crisis,maintain their mental health and plan their future with hope.
## Software Design

![ERD Graph](https://user-images.githubusercontent.com/77119427/106505220-e5b04e00-64bf-11eb-9fa1-085fbf1f631c.PNG)

* User Function
  * Username (as Login)
  * First_name
  * Last_name

* Creating an Post-Covid budget/todo List
  * an unique List ID
  * Username 
  * Number of items in the List 
  * Total costs in the List 

* Todo item Function
  * Todo item will be sorted by Todo List_ID
  * Preference,Description and Title, costs can be inputted by user via UI
  * Details of the items can be viewed, updated and deleted under the Todo List
  * Date of the activities will be recorded and displayed on UI and stored in the database.

* Budget Summary Function
  * Unique Budget ID
  * Username
  * Balance based on the budget activities

* Ledger Function
  * Unique event_id 
  * the event is sorted by Budgeter_ID
  * Action log included the options of withdraw and deposit of savings 
  * Value_in_GBP for the user to input the amount of their savings
  * user can create, input, and view their saving activities and balance in this section of the web app.

* Account Summary 
 * in this section of the web app, user can view the summary of all their planning and saving activities.
 * Basic data calculation and performance ratio will be generated and updated for view

The web app design has included Budget Summary and Todo List to have one to one relationship with the Users table and one to many relationship with the Ledger and Todo Item tables through data normalisation. 

The advantages of such design is that the design avoids directly connecting Ledger 
Table and Todoitem table with the users tables, so that in the future if there are any additional features of the app in adding multiple budget plans and todo lists of the same user (developing one to many relationship), the application and the database can be easily further developed to adjust to these new features without restructuring, compromising app functions and risking corrupting the database. Hence, it is suggested that the design can provide a more sustainable solution for the future improvement of the app.




## Programming/Software Development

The coding process is strictly in line of Single Responsibility Principle (SRP), PEP 8 Style Guide for Python Code, various documentations, the agile development approach and various naming conventions in order to exercise and demonstrate the best practice of the programming development. The coding structure is as followed:

* app.py              -- as Controller 
* data_access.py      -- Data access layer for database
* user.py             -- WTForm used for UI

The structure and the functions have been refactored more than three times in order to produce more readable and reusable codes and to fulfil the Single Responsibility Principle (SRP).

The codes was reviewed, debugged and tested constantly throughout programming and development, errors and exceptions were identified and handled. 

In following SFIA 7 framework and the Agile approach, the project consists of 1 sprint, 4 epics, 12 stories, 5 spikes (More details please see issues and milestone of the github project broad). The coding process was developed along with each feature/ user stories mentioned below  under an feature branch. The feature were completed, tested to be working and thereafter merge with the main branch of the repository. 


![Kanban Board](https://user-images.githubusercontent.com/77119427/107135112-ec8bf600-68ef-11eb-80bf-c7d02d291602.png)


## Testing
Testing is conducted via Pytest, all tests all passed, it provided 86% coverage over 290 application statements. There are 47 passed unit tests covering different scenarios with different types of expected outcomes, they are readable, fast and reliable. Further exception handling were added on the source code for improvement as the results of the testing. 

The unit testing is needed to be  connected to an actual instance of the sql server database. Pipeline was set up to utilise a test server for this purpose - i.e. the Database gets dropped & I publish it fresh in the CI pipeline prior to executing unit-tests. Further to this  Pytest fixtures was set up to run pre- & post- test to setup & tear down data in the Database consumed by each unit test.

![Unit testing CovReport](https://user-images.githubusercontent.com/77119427/107135192-615f3000-68f0-11eb-931f-886c5e96ea88.png)

It is encouraged that an TDD approach of testing to be implemented in this project. However, it is widely accepted that the purpose of a unit test in software engineering is to verify the behavior of a relatively small piece of software, independently from other parts. Unit tests are narrow in scope, and allow us to cover all cases, ensuring that every single part works correctly.

The testing method in this project and the constraints of using SQLalchemy along with Flask with external database such as SQL server has limited the options of exercising unit testing, as an consequences, the test is conducted on the basis that an external connection of an database must be established, it is suggested that the unit testing under such circumstances is very much alike integration testing, where it demonstrate how the app behave in the real-life environment. 


## Systems Integration and Build
* AWS RDS Relational Database Service  was used to deploy SQL server database 
* Environmental variable was set for the cconnection between RDS and web app
* Amazon Elastic Compute Cloud was used to host CI server Jenkins and deploy the application 
* Jenkins is used to achieve Continuous Integration by building an automated project
* Enviorment variable was built, virtual enviorment was activated for testing the application
* Application was tested automatically via Jenkins
* Deploymennt was achieved by exporting, and deploying Python package as artifact to AWS EC2 and the web app become operative and avaliable for further development and deplloyment.
* The build was successful as evidenced on github project issue # 7( details see https://github.com/AbbyXSu/Bucket_List_Budgeter/issues/7#issuecomment-774941862 )

## Risk Assessment
* SQL injection might be a cybersecurity risk factor in operating this web appplication as the database is directly managed under Python ORM tool SQLAlchemy, the solution is to put limited permission to SQLAlchemy using state driven database approach and have seperate database manaagement systerm, however, further security measure are needed for further development and deployment.
* Http attack and data breach is also possible to happen when the connection of the application become vulnerable when hosting on an VM, the solution is to make sure sensitive information of the users are encryted and stored seperately from the hosting enviorment and give normal users; limited permission to them.Hoewever, it is critial that the users should have the awareness to avoid posting sensitive information on the application.
* SQL server connection goes down, in the event when SQL server on AWS EDS goes down, the application will become unfunctional. The solution is to create an new RDS connection, or contact the service provider AWS.
* Web server technical issues or suffers attacks, in which case the the web application will become not funtional, an back up web server/VM might be needed to be created. If issue presists, contacting the service provider AWS.
* The application is also exposed to a certain degree of security risk as password authentications is provided.
* Intergration testing and performance testings might be needed to explore the appllication's performance in real life pratice.


## Future Improvements
* Bucket List can be extended to multiple bucket list per user (To travel List/Todo with friends List etc.)
* Budget Summary can be extended to multiple Budgets per user( Travel budget/ Party Budget etc.)
* user authentications via password
* Better UI for better user experience 
* Graph and Chart can be introduced for analytical functions for the users

Author

Abby X Su

Acknowledgements

QA Academy for the teaching and support so I can carry out this project successfully.
My dearest friends and family who inspired and supported me throughout the project.
