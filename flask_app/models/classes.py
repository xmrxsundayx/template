# import the function that will return an instance of a connection
from mysqlconnection import connectToMySQL
# model the class after the <!table name!> table from our database
class Friend:
    # ... other class methods
    DB = "first_flask"
    #make your schema a variable for reusablity. (BEST PRACTICE)
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.occupation = data['occupation']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # class method to save our friend to the database
    @classmethod
    def save(cls, data ):
        #possible database variable (in this case it would be db= 'first_flask')
        query = "INSERT INTO friends ( first_name , last_name , occupation , created_at, updated_at ) VALUES ( %(fname)s , %(lname)s , %(occ)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('first_flask').query_db( query, data )
        #connectToMySQL name of your schema unless you define it as a variable then if would be (cls.db) 

        #sample of queries with data
        query = """UPDATE <!table name!> SET <!column name>=%(fr)s 
            WHERE id=%(id_nam)s;"""
        data = {
            "fn": #possibly a value from a form,
            "id_num" #ends with ( : )possibly a value from the url
        }


    
    #***CREATE***

    # (2)the save method will be used when we need to save a new friend to our database
    @classmethod
    def save(cls, data):
        query = """INSERT INTO friends (first_name,last_name,occupation)
            VALUES (%(first_name)s,%(last_name)s,%(occ)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result


    #***READ***

        # the get_all method will be used when we need to retrieve all the rows of the table 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM friends;"
        results = connectToMySQL(cls.DB).query_db(query)
        friends = []
        #appending data from the database will be appended into a list. so you need a variable with a list to store it in
        for friend in results:
            friends.append( cls(friend) )
        return friends

        # the get_one method will be used when we need to retrieve just one specific row of the table
    @classmethod
    def get_one(cls, friend_id):
        query  = "SELECT * FROM friends WHERE id = %(id)s";
        #when you get information back from the database it will come in the form of a dictionary
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    #***UPDATE***
        
    # the update method will be used when we need to update a friend in our database
    @classmethod
    def update(cls,data):
        query = """UPDATE friends 
                SET first_name=%(first_name)s,
                last_name=%(last_name)s,email=%(email)s 
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    #***DELETE***

        # the delete method will be used when we need to delete a friend from our database
    @classmethod
    def delete(cls, friend_id):
        query  = "DELETE FROM friends WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)