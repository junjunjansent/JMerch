class APIError(Exception):
    def __init__(self, status, title, detail, pointer="unknown"):
        self.status = status
        self.pointer = pointer
        self.title = title
        self.detail = detail
    
def raise_api_error(err, status = 500, title = "Internal Server Error", pointer = "unknown"):
    if isinstance(err, APIError):
        raise err
    else:
        err_name = err.__class__.__name__
        raise APIError(
            status={status},
            title=f"{title}: {err_name}",
            detail=str(err), 
            pointer=f"{pointer}")


# raise APIError(400, "Bad Request", "Missing email")

                #    "status": 409,
#             "source": { "pointer": "public_controller.py" },
#             "title": "Conflict: User Exists",
#             "detail": "Username already taken.",

