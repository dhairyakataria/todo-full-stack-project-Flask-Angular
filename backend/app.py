from todo import app, db
# @app.route('/', methods = ['GET', 'POST'])
# def home():
#     return "home working"


# @app.route("/users/create", methods=["GET", "POST"])
# def user_create():
#     if request.method == "POST":
#         user = Users(
#             username=request.form["username"],
#             email=request.form["email"],
#             password = request.form["password"]
#         )
#         db.session.add(user)
#         db.session.commit()
#         return f"{user}"

#     return "error"


with app.app_context():
    print("creating db ----------------")
    db.create_all()
