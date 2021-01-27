


# @app.route("/update", methods=["POST"])
# def update():
#     person = users.query.filter_by(name=request.form.get("oldname")).first()
#     person.name = request.form.get("newname")
#     db.session.commit()
#     return redirect("/")

# @app.route("/delete", methods=["POST"])
# def delete():
#     person = users.query.filter_by(name=request.form.get("name")).first()
#     db.session.delete(person)
#     db.session.commit()
#     return redirect("/")

