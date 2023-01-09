class printHeader:
    def __init__(self, get_response):
        self.get_response = get_response
        # ここに処理を記述すると、サーバーが起動したときのみ実行される

    def __call__(self, request):
        # ここに処理を記述すると、view関数が実行される前に実行される
        # print("■request.METAの表示")
        # print(dir(request))
        # print(request.COOKIES["refresh_token"])
        # nowtoken = {"refresh_token": request.COOKIES["refresh_token"]}
        # print(nowtoken)
        # print(request.headers)
        # for key in request.META:
        #     print(key)
        # print(dir(request))
        # print(request.)

        # print("■HTTP_ORIGIN：", end="")
        # print(request.META.get("HTTP_ORIGIN"))
        # print("■HTTP_COOKIE：", end="")
        # print(request.META.get("HTTP_COOKIE"))

        # print(request.accepts)
        # print("■request.data表示")
        # print(request.body)
        # print("■request.user：", end="")
        # print(request.user)
        # print(request.data)
        response = self.get_response(request)
        # print("request")

        # print("■request.user：", end="")
        # print(request.user)
        # print(request.user.is_authenticated)

        # for key in response.cookies.keys():
        #     print(key)
        # ここに処理を記述すると、view関数が実行された後に実行される
        # print("■responce：", end="")
        # print(dir(response))
        return response
