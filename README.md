# FlaskProject

The software I am testing is very similar to the ST sample project but remade from scratch in Python. It is a web server which can be used through a website UI or direct http requests. It provides a system for user registration, login, profile editing and usage allowing users to order boxes from an imaginary food shop. The system also has different user access levels for regular users and admins with additional functions and removed restrictions for admin users.

The program uses Python with ```Flask``` for the webserver and ```SQLAlchemy``` with ```SQLite``` for the database which stores user and order information.

The ```unittest``` library is used for unit and integration testing. Additionally ```Locust``` is used for load testing and ```Coverage``` was used to calculate test coverage.
