from rest_framework.schemas.openapi import AutoSchema
from .serializers import YearSerializer

class YearSchema(AutoSchema):
    def get_operation(self, path, method):
        operation = super().get_operation(path, method)
        if method.lower() == "post":
            request_body = {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": YearSerializer().to_schema(),
                    }
                },
            }
            if "requestBody" not in operation:
                operation["requestBody"] = request_body
            else:
                operation["requestBody"].update(request_body)
        return operation