from flask import Response
import json

class JsonResponse:
    def getResponse(data,statusMessage,statusCode):
        if data == None:
            return Response(
                json.dumps({"data": None, "statusMessage": statusMessage, "statusCode": statusCode}),
                mimetype="application/json",
            )
        else:
            return Response(
                json.dumps({"data": data, "statusMessage": statusMessage, "statusCode": statusCode}),
                mimetype="application/json",
            )