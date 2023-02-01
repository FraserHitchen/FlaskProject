
# Requirements
## Stakeholders and Requirements:
-   Users
	-   Want to be able to order quickly so quick account creation is a must.
	-   Want their passwords and any other private information stored securely.
	-   Want to be able to update their information easily.
	-   Want to add or update and order easily.

-   Admins
	-   Want to be able to get information on all users or specific users quickly no matter how many users there are.
	-   Want to be able to get information on all orders of a specific user quickly no matter how many orders they have.
	-   Want to be able to delete users.
	
Broken down into the different range of requirements:
	
- Functional Requirements:
	- Users will be able to register an account, log in, and then place an order using that account.
	- Users can edit the information on their account such as email and address.
	- Admins will be able to get information on users and orders, and will be able to edit and delete the orders of users.

- Measurable Quality Attributes:
	- Correctness: The functions of the software should work as expected.
	- Performance: The software should run well even under stress.
    
- Qualitative Requirements:
	- Correctness: The functions of the software should work as expected.
	- Usability: The software should be user-friendly and easy to learn and understand.
	- Robustness: The system should continue to work with limited behaviour under extreme conditions.
	- Security: User’s personal information should be kept securely.



    
Sorting the requirements by level:

### Functional Testing
-   Unit Testing
	-   Users
		-   Will be able to make an account. 
		-   Will be able to login to their account. 
		-   Will be able to view their own account information. 
		-   Will be able to update account information.  
		-   Will be able to add an order. 
		-   Will be able to update their own orders. 
		-   Will be able to delete their own orders.

	-   Admins
		-   Will be able to get information on all users.
		-   Will be able to get information on a specific user. 
		-   Will be able to delete users.  
		-   Will be able to get information on all orders of a specific user.  
		-   Will be able to get information on a specific order. 
		-   Will be able to delete orders. 
		-   Will be able to edit orders.
	-  Database
		- Able to add records.
		- Able to edit records.
		- Able to delete records.
		
-   Integration Testing
	- Registered users are added to a database.
	- Logging in validates the users password again one stored in the databse.
	- User information in the database can be edited through the UI.
	- Placed orders are added to the database.
	- Orders in the database can be edited by users and admins.

-   System Testing
	- The UI is intuitive to use.
	- The system works under load.
	- All functions give the correct responses.
	- User information is kept securely.
