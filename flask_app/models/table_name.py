# import the function that will return an instance of a connection
from mysqlconnection import connectToMySQL
# model the class after the <!table name!> table from our database
class Rides:

    DB = "DB NAME"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posting_user= None

    #***CREATE***

    @classmethod
    def save(cls, data ):
        query = """INSERT INTO 
                    Table_name ( first_name , last_name , email, password) 
                    VALUES 
                    ( %(first_name)s , %(last_name)s , %(email)s , %(password)s)
                    ;"""
        return connectToMySQL(cls.DB).query_db( query, data )

    #***READ***

    @classmethod
    def get_all(cls):
        query = """SELECT * FROM 
                    Table_name
                    ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        tables = []
        for table in results:
            tables.append( cls(table) )
        return tables

    @classmethod
    def get_one(cls, data):
        query  ="""
                    SELECT * FROM 
                    tables 
                    WHERE 
                    id = %(id)s
                    ;"""
        #when you get information back from the database it will come in the form of a dictionary
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    # *****ONE TO MANY*****

    @classmethod
    def get_show_by_user(cls, data):
        query = """
                    SELECT * FROM 
                    posts 
                    LEFT JOIN 
                    users 
                    ON 
                    posts.user_id = users.id 
                    WHERE 
                    posts.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        for row in results:
            show = cls(row)
            user_data = {
                'id': row["users.id"],
                'first_name': row["first_name"],
                'last_name' : row["last_name"],
                'email' : row["email"],
                'password' : row['password'],
                'created_at' : row["created_at"],
                'updated_at' : row["updated_at"], }
            show.user_name = user_models.Users(user_data)
            print(show.user_name.first_name)
        return show

    @classmethod
    def get_by_id(cls,data):
        query="""
                    SELECT * FROM
                    tables
                    JOIN
                    users
                    ON
                    tables.user_id = users.id
                    WHERE
                    tables.id = %(id)s
                    ;"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        for row in result: 
            one_table = cls(row)
            posting_user ={
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']}
            one_table.posting_user = users_mod.Users(posting_user)
        return one_table



# controller text
#         one_user = get_one_user_many_posts(id)
# for posts in one_user.posts:
# posts.postAttributes



# when using %()s then method must bring in data as well. b/c it is reading in key value pairs
# viewing all posts by one single user, using a JOIN to bring together the tables and only the posts that are from one user id 
    @classmethod
    def view_all_of_one_users_posts(cls):
        query = """ SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.id DESC;"""
        results = connectToMySQL(cls.DB).query_db(query)
        all_posts = []
        for row in results:
            one_post= cls(row)
            user_data={
                'id': row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email': row['email'],
                'password': row['password'],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            one_post.user_name = Table1_classes.Table_name(user_data)
            all_posts.append(one_post)
        return all_posts


# alternate way -- clean code way, getting one user with many things -- only works when selecting one user with many things. 
    @classmethod
    def get_one_user_many_posts(cls, data):
        query = """ SELECT * FROM users LEFT 
        JOIN posts ON users.post_id = posts.id WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        user_info = Table1_classes.Table_name(results[0]) 
        # user is now instanciated 
        # 1 - now need to itterate through results in order to instanciate
        # 2- parse through post data
        for x in results:
            post_data= {
                'id': x['id'],
                'foreign_key_id' : x['foreign_key_id'],
                'column_name1' :  x['column_name1'],
                'column_name2' :  x['column_name2'],
                'created_at' :  x['created_at'],
                'updated_at' :  x['updated_at']
            }
            user_info.posts.append(cls(post_data))
        return user_info
    # query-left joining b/c we are getting one user, and we want the first dictiionary to be user
    # results is equal to a list of dict where the first item is our user. 
    # bc users is the first item in results we can confiently instanciate a user by indexing results[0]
    # itterate through results and parse post_data inside of for loop. 
    # we access the user objects empty list of posts (self.posts in Table_name class)
    # and append and instanciate each post related to that particular user --all in one line
    # then return user info! which gives access to the user and user.post list
    # also allows us to itterate through with jinja


# get one post by one user using LEFT JOIN to bring together the tables
    @classmethod
    def get_post_by_user(cls, data):
        query = """ SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE posts.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        for row in results:
            post = cls(row)
            user_data = {
                'id': row["users.id"],
                'first_name': row["first_name"],
                'last_name' : row["last_name"],
                'email' : row["email"],
                'password' : row['password'],
                'created_at' : row["created_at"],
                'updated_at' : row["updated_at"], }

            post.user_name = Table1_classes.Table_name(user_data)
            print(post.user_name.first_name)
        return post


    #***UPDATE***

    @classmethod
    def update(cls,data):
        query ="""
                    UPDATE 
                    table 
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
        table 
        WHERE 
        id = %(id)s
        ;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results



# *****VALIDATION*****

    @staticmethod
    def verify_shows(data):
        is_valid =True
        if len(data['title'])<3:
            flash('Title is required')
            is_valid = False
        if len(data['description'])<3:
            flash('Description is required')
            is_valid = False
        if len(data['network'])<3:
            flash('Network is required')
            is_valid = False
        return is_valid