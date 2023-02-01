
# LO1
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
    
With these in mind we can sort these requirements by level:

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
		
-   Integration Testing
	-   Users
		-   Will be able to register an account, log in, and then place an order using that account.
		-   Will be able to place an order and then edit that order.
		-   Will be able to view their own account information and then update it.

	-   Admins
		-   Will be able to get information on a specific user and then find all orders from that user.
		-   Will be able to get information on a specific order and then view the information of the user who ordered it. 
		-   Will be able to view all orders and then edit or delete specific ones.

-   System Testing
	-   Users
		-   Will be able to create, login to, manage, and delete their account using the account subsystem.
		-   Will be able to place, edit and delete their orders using the order subsystem.
   
	-   Admins
		-   Will be able to view and manage user accounts using the account subsystem.
		-   Will be able to view, edit and delete user orders using the orders subsystem.

### Non-Functional Testing
-   Security
	-   User’s personal information should be kept securely.
	-   User passwords should be encrypted.
	   
-   Reliability
	-   The system should complete all functions without failure.
   
-   Usability
	-   Performing functions through the system should be easy.
   
-   Robustness
	-   The system should continue to work with limited behaviour under extreme conditions.
   
-   Performance
	-   All functions in the system should work quickly even under high load.
    

  

### Testing Approaches

Unit Testing
-   To perform the unit testing I will create automated functions in code to test each of the components of the system in isolation. For each test I will write a variety of test cases and then use assertions to verify the expected output.
    

Integration Testing
-   For the integration testing I will use a big-bang approach of integrating all modules at once and testing them all as one unit. Since I have knowledge of how the code works this will be a white-box testing approach.
    

System Testing
-   For the system testing I will use end-to-end testing to test the workflow of each subsystem and well as the overall system. I will additionally conduct performance and stress testing to test the non-functional requirements of the system.
    

### Approach Assessment

Unit Testing
-   With unit testing it is usually better to perform test-driven development where tests are written before the code but since the components of the system are already written this is an appropriate approach to unit testing.
    

Integration Testing
-   There are several approaches to integration but I chose big-bang testing due to all of the units already being integrated and the small size of the system. Big-bang is good for small systems as it allows for easy detection of integration issues and is generally quicker than other approaches.
-   The main disadvantages of big-bang testing is that it is slow for large systems with many units and that locating the source of an issue can be difficult, but these are mostly mitigated in a system of this size so I believe this approach is sufficient.
    

System Testing
-   I believe that end-to-end testing is an appropriate way to test on this system however there are some limitations. Ideally this testing would be performed with a black-box approach by someone with no knowledge of the underlying systems in order to get an unbiased runthrough the system.
-   Additionally I will be limited in the amount of non-functional requirements I can test since I can only test the system on my own machine and I don’t have the data or ability to meaningfully test the security of the system or put it under an extremely large load.
