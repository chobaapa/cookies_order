# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Cookie_order:

    DB = "cookie_order"

    def __init__(self,cookies):

        self.id = cookies["id"]
        self.name = cookies["name"]
        self.cookie = cookies["cookie"]
        self.amount = cookies["amount"]
        self.created_at = cookies["created_at"]
        self.updated_at = cookies["updated_at"]

    @classmethod
    def is_valid(cls, cookies):
        valid = True

        if len(cookies["name"]) <= 0 or len(cookies ["cookie_type"]) <= 0 or len(cookies["amount"]) <= 0:
            valid = False
            flash("All fields required")
            return valid
        if len(cookies ["name"]) < 2:
            valid = False
            flash("Name must be at least 2 characters")
        if len(cookies["cookie"]) < 2:
            valid = False
            flash("Cookie type must be at least 2 characters")
        if int(cookies["amount"]) <= 0:
            valid = False
            flash("Please enter a valid number of boxes.")
        return valid
    
    @classmethod
    def get_by_id(cls, order_id):
        query = "SELECT * from cookies WHERE id = %(id)s;"
        data = {
            "id": order_id
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            order = result[0]
            return order

        return False

    @classmethod
    def get_all(cls):
        query = "SELECT * from cookies;"
        orders_data = connectToMySQL(cls.DB).query_db(query)

        orders = []
        for order in orders_data:
            orders.append(cls(order))

        return orders

    @classmethod
    def create(cls, cookie_order):

        query = """
                INSERT into cookies (name, cookie_type, num_boxes)
                VALUES (%(name)s, %(cookie_type)s, %(num_boxes)s);"""

        result = connectToMySQL(cls.DB).query_db(query, cookie_order)
        return result


    @classmethod
    def update(cls, cookie_order):

        query = """
                UPDATE cookies
                SET name = %(name)s, cookie_type = %(cookie_type)s, num_boxes = %(num_boxes)s
                WHERE id = %(id)s;"""

        result = connectToMySQL(cls.DB).query_db(query, cookie_order)
        return result