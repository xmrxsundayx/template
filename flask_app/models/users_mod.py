from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Users:

    DB = "DATABASE NAME"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #***CREATE***

    @classmethod
    def save(cls, data ):
        query = """INSERT INTO 
                    users ( first_name , last_name , email, password) 
                    VALUES 
                    ( %(first_name)s , %(last_name)s , %(email)s , %(password)s)
                    ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    #***READ***

    # @classmethod
    # def get_all(cls):
    #     query = """SELECT * FROM 
    #                 users
    #                 ;"""
    #     results = connectToMySQL(cls.DB).query_db(query)
    #     users = []
    #     for user in results:
    #         users.append( cls(user) )
    #     return users

    @classmethod
    def get_one(cls, data):
        query  ="""
                    SELECT * FROM 
                    users 
                    WHERE 
                    id = %(id)s
                    ;"""
        #when you get information back from the database it will come in the form of a dictionary
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query="""
                    SELECT * FROM
                    (((star table)))
                    JOIN
                    users
                    ON
                    (((star table))).user_id = users.id
                    WHERE
                    (((star table))).id = %(id)s
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        for row in result: 
            one_show = cls(row)
            posting_user ={
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
        }
            one_show.posting_user = users_mod.Users(posting_user)
        return one_show

    #***UPDATE***

    @classmethod
    def update(cls,data):
        query ="""
                    UPDATE 
                    users 
                    SET 
                    first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s 
                    WHERE 
                    id = %(id)s
                    ;"""
        results = connectToMySQL(cls.DB).query_db(query,data)
        return results

    #***DELETE***

    @classmethod
    def delete(cls, data):
        query  ="""
        DELETE FROM 
        users 
        WHERE 
        id = %(id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    #***VALIDATION***

    @staticmethod
    def validate_user(user):
        is_valid = True
        data = {'email': user['email']}
        valid_user= Users.get_user_by_email(data)

        if valid_user:
            flash('Email is already in use! Try logging in.', 'reg')
            is_valid=False
        if len(user['first_name'])< 2:
            flash('First name must be at least 1 character.','reg')
            is_valid = False
        if len(user['last_name'])< 2:
            flash('Last name must be at least 1 character','reg')
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email','reg')
            is_valid=False
        password = user['password']
        if len(password) < 8:
            flash('Password must be at least 8 characters long.','reg')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('Passwords do not match','reg')
            is_valid=False
        return is_valid

# *****COMPLEX PASSWORD VERIFICATIONS*****

    # @staticmethod
    # def validate_user(user):
    #     is_valid = True
    #     data = {'email': user['email']}
    #     valid_user= Users.get_user_by_email(data)

    #     if len(user['first_name'])< 2:
    #         flash('First name must be at least 1 character.','reg')
    #         is_valid = False
    #     if len(user['last_name'])< 2:
    #         flash('Last name must be at least 1 character','reg')
    #         is_valid=False
    #     if valid_user:
    #         flash('Email is already in use! Try logging in.', 'reg')
    #         is_valid=False
    #     if not EMAIL_REGEX.match(user['email']):
    #         flash('Invalid email','reg')
    #         is_valid=False
    #     password = user['password']
    #     if len(password) < 8:
    #         flash('Password must be at least 8 characters long.','reg')
    #         is_valid = False
    #     else:
    #         missing_reqs = []
    #         if not re.search(r"[a-z]", password):
    #             missing_reqs.append("lowercase letter")
    #         if not re.search(r"[A-Z]", password):
    #             missing_reqs.append("uppercase letter")
    #         if not re.search(r"[0-9]", password):
    #             missing_reqs.append("digit")
    #         if missing_reqs:
    #             flash(f"Password is missing the following required character types: {', '.join(missing_reqs)}",'reg')
    #             is_valid = False
    #     if user['confirm_password'] != user['password']:
    #         flash('Passwords do not match','reg')
    #         is_valid=False
    #     return is_valid