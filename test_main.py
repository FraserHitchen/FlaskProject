from unittest import TestCase

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import unittest
from main import app, db, users, orders
from flask_testing import TestCase

app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
# db = SQLAlchemy(app)


# class users(db.Model):
#     _id = db.Column("id", db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     password = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)
#     address = db.Column(db.String(100))
#     admin = db.Column(db.Boolean, unique=False, default=False)
#
#     def __init__(self, name, password, email, address, admin):
#         self.name = name
#         self.password = password
#         self.email = email
#         self.address = address
#         self.admin = admin
#
#
# class orders(db.Model):
#     _id = db.Column("id", db.Integer, primary_key=True)
#     user_id = db.Column("user_id", db.Integer)
#     type = db.Column(db.String(100))
#     description = db.Column(db.String(100))
#
#     def __init__(self, user_id, type, description):
#         self.user_id = user_id
#         self.type = type
#         self.description = description


class FlaskTestCase(TestCase):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def create_app(self):
        return app

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        # db.create_all()

    def tearDown(self):
        self.app = None
        #db.session.remove()
        #db.drop_all()

    def test_home(self):
        tester = app.test_client()
        response = tester.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test1234", response.data)

    def test_user_functions(self):
        with app.test_client() as tester:
            # Reset users and orders
            response = tester.get("/reset", content_type="html/text")

            # Register a user
            response = tester.post("/register", data={"name": "John", "password": "hunter2", "email": "John@gmail.com",
                                                      "address": "123 Main St"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Registration Successful!", response.data)

            # Logout
            response = tester.get("/logout", content_type="html/text")
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"You have been logged out, John", response.data)

            # Try to logout while already logged out
            response = tester.get("/logout", content_type="html/text")
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"You are not logged in!", response.data)

            # Try to login with wrong password
            response = tester.post("/login", data={"name": "John", "password": "wrong"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Incorrect name or password!", response.data)

            # Log back in
            response = tester.post("/login", data={"name": "John", "password": "hunter2"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Login Successful!", response.data)

            # Try to login while already logged in
            response = tester.post("/login", data={"name": "John", "password": "hunter2"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Already Logged In!", response.data)

            # Edit User Details
            response = tester.post("/user",
                                   data={"name": "Johnny", "email": "John@gmail.co.uk", "address": "134 Side St."})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Name was saved.", response.data)
            self.assertIn(b"Email was saved.", response.data)
            self.assertIn(b"Address was saved.", response.data)
            self.assertEqual(session["name"], "Johnny")
            self.assertEqual(session["email"], "John@gmail.co.uk")
            self.assertEqual(session["address"], "134 Side St.")

            # Attempt to access Admin page
            response = tester.get("/admin", content_type="html/text")
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"You do not have permission to access this page!", response.data)

            # Place Order
            response = tester.post("/order", data={"type": "Box1"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Order Successful!", response.data)
            self.assertIn(b"Order ID: 1", response.data)
            self.assertIn(b"Box1", response.data)

            # Try to edit non-existing order
            response = tester.post("/order", data={"id": "2"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"No order with that ID was found.", response.data)

            # Edit Order
            response = tester.post("/order", data={"id": "1"})
            self.assertEqual(response.status_code, 200)
            response = tester.post("/order", data={"new_type": "Box2"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Order ID: 1", response.data)
            self.assertIn(b"Box2", response.data)

            # Delete Order
            response = tester.post("/order", data={"id": "1"})
            self.assertEqual(response.status_code, 200)
            response = tester.post("/order", data={"delete": "Delete Order"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Order was deleted.", response.data)
            self.assertNotIn(b"Order ID: 1.", response.data)

            # Logout
            response = tester.get("/logout", content_type="html/text")
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"You have been logged out, John", response.data)

    def test_admin_functions(self):
        with app.test_client() as tester:
            # Reset users and orders
            response = tester.get("/reset", content_type="html/text")

            # Register a non-admin user
            response = tester.post("/register", data={"name": "John", "password": "hunter2", "email": "John@gmail.com",
                                                      "address": "123 Main St"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Registration Successful!", response.data)

            # Place Order
            response = tester.post("/order", data={"type": "Box1"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Order Successful!", response.data)
            self.assertIn(b"Order ID: 1", response.data)
            self.assertIn(b"Box1", response.data)

            # Logout
            response = tester.get("/logout", content_type="html/text")
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"You have been logged out, John", response.data)

            # Register an admin user
            response = tester.post("/register",
                                   data={"name": "Fraser", "password": "admin123", "email": "Fraser@gmail.com",
                                         "address": "26 Main Lane", "admin": True})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Registration Successful!", response.data)

            # Access Admin page
            response = tester.get("/admin", content_type="html/text")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"ID: 1, Name: John, Email: John@gmail.com, Address: 123 Main St, Admin: False",
                          response.data)
            self.assertIn(b"ID: 2, Name: Fraser, Email: Fraser@gmail.com, Address: 26 Main Lane, Admin: True",
                          response.data)

            # Search for a specific User's information
            response = tester.post("/admin", data={"id": "1"})
            self.assertEqual(response.status_code, 200)
            # Check that the information for John is there twice, once from the list of all users and once for the
            # individual search
            assert response.data.count(
                b"ID: 1, Name: John, Email: John@gmail.com, Address: 123 Main St, Admin: False") == 2

            # Search for a non-existing user's information
            response = tester.post("/admin", data={"id": "5"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"No user with that ID could be found!", response.data)

            # Search for a specific user's orders
            response = tester.post("/admin", data={"uo_id": "1"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"ID: 1, User ID: 1, Type: Box1, Description:", response.data)

            # Search for a non-existing user's orders
            response = tester.post("/admin", data={"uo_id": "5"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"No orders from that user were found.", response.data)

            # Search for orders from a user who has no orders
            response = tester.post("/admin", data={"uo_id": "2"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"No orders from that user were found.", response.data)

            # Search for a specific order
            response = tester.post("/admin", data={"order_id": "1"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"ID: 1, User ID: 1, Type: Box1, Description:", response.data)

            # Search for a non-existing order
            response = tester.post("/admin", data={"order_id": "2"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"No order with that ID could be found!", response.data)

            # See all orders
            response = tester.post("/admin", data={"see_all": "See All Orders"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"ID: 1, User ID: 1, Type: Box1, Description:", response.data)

            # Edit a user's order
            response = tester.post("/order", data={"id": "1"})
            self.assertEqual(response.status_code, 200)
            response = tester.post("/order", data={"new_type": "Box2", "new_desc": "Changed By Admin"})
            self.assertEqual(response.status_code, 200)

            # Check that order was updated
            response = tester.post("/admin", data={"order_id": "1"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"ID: 1, User ID: 1, Type: Box2, Description: Changed By Admin", response.data)

            # Delete user's order
            response = tester.post("/order", data={"id": "1"})
            self.assertEqual(response.status_code, 200)
            response = tester.post("/order", data={"delete": "Delete Order"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Order was deleted.", response.data)

            # Check that order was deleted
            response = tester.post("/admin", data={"order_id": "1"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"No order with that ID could be found!", response.data)

    def test_database(self):
        # Add User
        user = users("TestUser", "Password123", "Test@gmail.com", "123 Test St.", True)
        db.session.add(user)
        db.session.commit()

        result = users.query.filter_by(name="TestUser").first()
        assert result is not None
        assert result.name == "TestUser"

        # Update User
        found_user = users.query.filter_by(name="TestUser").first()
        found_user.name = "Updated"
        found_user.admin = False
        db.session.commit()

        result = users.query.filter_by(name="Updated").first()
        assert result is not None
        assert result.name == "Updated"
        assert result.password == "Password123"
        assert result.admin is False

        # Delete User
        users.query.filter_by(name="Updated").delete()
        db.session.commit()

        result = users.query.filter_by(name="Updated").first()
        assert result is None

        # Add Order
        order = orders("1", "Box1", "TestDesc")
        db.session.add(order)
        db.session.commit()

        result = orders.query.filter_by(user_id="1", type="Box1", description="TestDesc").first()
        assert result is not None
        assert result.description == "TestDesc"

        # Update Order
        found_order = orders.query.filter_by(user_id="1", type="Box1", description="TestDesc").first()
        found_order.user_id="5"
        found_order.description="Updated"
        db.session.commit()

        result = orders.query.filter_by(user_id="5", type="Box1", description="Updated").first()
        assert result is not None
        assert result.user_id == 5
        assert result.type == "Box1"
        assert result.description == "Updated"

        # Delete Order
        orders.query.filter_by(user_id="5", type="Box1", description="Updated").delete()
        db.session.commit()

        result = orders.query.filter_by(user_id="5", type="Box1", description="Updated").first()
        assert result is None

    def test_integration(self):
        with app.test_client() as tester:
            # Reset users and orders
            response = tester.get("/reset", content_type="html/text")

            # Register a user
            response = tester.post("/register", data={"name": "John", "password": "hunter2", "email": "John@gmail.com",
                                                      "address": "123 Main St"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Registration Successful!", response.data)

            # Check database integration
            result = users.query.filter_by(name="John").first()
            assert result is not None
            assert result.name == "John"
            db.session.commit()

            # Edit user details
            response = tester.post("/user",
                                   data={"name": "Johnny", "email": "John@gmail.co.uk", "address": "134 Side St."})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Name was saved.", response.data)
            self.assertIn(b"Email was saved.", response.data)
            self.assertIn(b"Address was saved.", response.data)
            self.assertEqual(session["name"], "Johnny")
            self.assertEqual(session["email"], "John@gmail.co.uk")
            self.assertEqual(session["address"], "134 Side St.")

            # Check database integration
            result = users.query.filter_by(name="Johnny").first()
            assert result is not None
            assert result.name == "Johnny"
            assert result.email == "John@gmail.co.uk"
            assert result.address == "134 Side St."

            # Add order
            response = tester.post("/order", data={"type": "Box1"})
            self.assertEqual(response.status_code, 302)
            response = tester.get(response.location)
            self.assertIn(b"Order Successful!", response.data)
            self.assertIn(b"Order ID: 1", response.data)
            self.assertIn(b"Box1", response.data)

            # Check database integration
            result = orders.query.filter_by(_id="1").first()
            assert result is not None
            assert result.type == "Box1"
            db.session.commit()

            # Edit order
            response = tester.post("/order", data={"id": "1"})
            self.assertEqual(response.status_code, 200)
            response = tester.post("/order", data={"new_type": "Box2"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Order ID: 1", response.data)
            self.assertIn(b"Box2", response.data)

            # Check database integration
            result = orders.query.filter_by(_id="1").first()
            assert result is not None
            assert result.type == "Box2"
            db.session.commit()

            # Delete order
            response = tester.post("/order", data={"id": "1"})
            self.assertEqual(response.status_code, 200)
            response = tester.post("/order", data={"delete": "Delete Order"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Order was deleted.", response.data)
            self.assertNotIn(b"Order ID: 1.", response.data)

            # Check database integration
            result = orders.query.filter_by(_id="1").first()
            assert result is None
            db.session.commit()


if __name__ == "__main__":
    unittest.main()
