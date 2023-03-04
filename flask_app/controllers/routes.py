from friend import Friend
#(1)retrieving and displaying data
@app.route('/')
def index():
    friends = Friend.get_all()
    print(friends)
    return render_template("index.html", all_friends = friends)

#***CREATE***

# relevant code snippet from server.py
@app.route('/create_friend', methods=["POST"])
def create_friend():
# First we make a data dictionary from our request.form coming from our template.
# The keys in data need to line up exactly with the variables in our query string.
    data = {
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "occ" : request.form["occ"]
        }
    # We pass the data dictionary into the save method from the Friend class.
    Friend.save(data)
        # Don't forget to redirect after saving to the database.
    return redirect('/')

#(2) this method uses the save function in classes to save the posted information to the database
@app.route('/friends/create', methods=['POST'])
#methods = ['POST'] is to restrict the HTTP methods that are allowed to access a particular route or endpoint in a Flask application.
def create():
    Friend.save(request.form)
#this says in the Friends class call on the save function with this infromation (request.form)
    return redirect('/')

#***READ***

@app.route('/')
def index():
    # calling the get_all method from the friends.py
    all_friends=Friend.get_all()
    # passing all friends to our template so we can display them there
    return render_template("index.html",friends=all_friends)


@app.route('/friend/show/<int:friend_id>')
def show(friend_id):
    # calling the get_one method and supplying it with the id of the friend we want to get
    friend=Friend.get_one(friend_id)
    return render_template("show_friend.html",friend=friend)

#***UPDATE***

@app.route('/friends/update',methods=['POST'])
def update():
    Friend.update(request.form)
    return redirect('/')

#***DELETE***

@app.route('/friends/delete/<int:friend_id>')
def delete(friend_id):
    Friend.delete(friend_id)
    return redirect('/')