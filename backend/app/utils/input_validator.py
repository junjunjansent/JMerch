# def validate_user_input(data):
#     errors = []

#     if not data.get("email"):
#         errors.append("Email is required.")
#     elif not re.match(r"^[-.\w]+@[-.\w]+\.[-.\w]{2,}$", data["email"]):
#         errors.append("Invalid email format.")

#     if not data.get("username") or len(data["username"]) < 4:
#         errors.append("Username must be at least 4 characters.")

#     return errors