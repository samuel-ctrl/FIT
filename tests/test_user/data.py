VALID_LOGIN_VIEW_API = (
    "/api/user/login",
    "post",
    {
        "email": "example.company@gmail.com"
    },
    {
        "status":200,
        "data":{"detail": "OTP sent successfully."}
    },
    {
        "mail":{
           "path" : "user.utils.custom_send_mail",
           "response": {"send": True, "message": "Mail send Successfully."}
        }
    }
)

