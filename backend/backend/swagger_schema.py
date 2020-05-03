from collections import OrderedDict
from urllib.parse import urlencode, unquote_plus
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from drf_yasg.inspectors.view import SwaggerAutoSchema, force_real_str
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi

tag_extra_data = {
    "Survey": {
        "name": "Survey",
        "description": """
""",
    },
    "Annotator": {
        "name": "Annotator",
        "description": """
""",
    },
    "Item": {
        "name": "Item",
        "description": """
""",
    },
}


class XCodeSampleAutoSchema(SwaggerAutoSchema):
    def process_string_parameter(self, parameter):
        min_length = getattr(parameter, "minLength", 10)
        max_length = getattr(parameter, "maxLength", 100)
        enum = getattr(parameter, "enum", None)
        format_map = {
            "date-time": timezone.now().isoformat(),
            "date": timezone.now().date().isoformat(),
            "time": timezone.now().time().isoformat(),
            "password": "*" * min_length,
            "none": "string"[:max_length]
            if min_length <= 6
            else ("string" * (min_length // 6))[:min_length],
        }
        if enum:
            return enum[0]
        return format_map[getattr(parameter, "format", "none")]

    def process_number_parameter(self, parameter):
        minimum = getattr(parameter, "minimum", 0)
        maximum = getattr(parameter, "maximum", 100)
        enum = getattr(parameter, "enum", None)
        if enum:
            return enum[0]
        elif minimum:
            return minimum
        elif maximum > 0:
            return 0
        else:
            return maximum

    def process_bool_parameter(self, _parameter):
        return True

    def generate_example_value(self, parameter):
        param_type = getattr(parameter, "type", "string")
        type_map = {
            "string": self.process_string_parameter,
            "number": self.process_number_parameter,
            "integer": self.process_number_parameter,
            "boolean": self.process_bool_parameter,
        }
        return type_map[param_type](parameter)

    def get_normalized_form_parameters(self):
        parameters = self.get_request_form_parameters(self.get_request_serializer())
        return OrderedDict(
            [
                (parameter.name, self.generate_example_value(parameter))
                for parameter in parameters
                if getattr(parameter, "required", False)
            ]
        )

    def get_normalized_query_parameters(self):
        parameters = self.get_query_parameters()
        return OrderedDict(
            [
                (parameter.name, self.generate_example_value(parameter))
                for parameter in parameters
            ]
        )

    def get_x_code_samples(self):
        payload = self.get_normalized_form_parameters()
        query = self.get_normalized_query_parameters()
        headers = {
            "Authorization": f"Bearer {get_random_string(30)}",
            "Accept": self.get_produces()[0],
        }
        url = unquote_plus(
            # pylint: disable=protected-access
            self.request._request.build_absolute_uri(self.path)
        )
        if "https" not in url:
            url = url.replace("http", "https")
        template_context = {
            "request_url": url,
            "method": self.method,
            "payload": payload,
            "query": query,
            "headers": headers,
            "query_format": urlencode(query, safe="/@"),
        }
        return [
            {
                "lang": "curl",
                "source": render_to_string(
                    "main/docs/langs/curl.html", template_context
                ),
            },
            {
                "lang": "python",
                "source": render_to_string(
                    "main/docs/langs/python.html", template_context
                ),
            },
            {
                "lang": "javascript",
                "source": render_to_string(
                    "main/docs/langs/javascript.html", template_context
                ),
            },
        ]

    def set_x_code_samples(self, operation):
        setattr(operation, "x-code-samples", self.get_x_code_samples())
        return operation

    def get_operation(self, operation_keys=None):
        consumes = self.get_consumes()
        produces = self.get_produces()

        body = self.get_request_body_parameters(consumes)
        query = self.get_query_parameters()
        parameters = body + query
        parameters = [param for param in parameters if param is not None]
        parameters = self.add_manual_parameters(parameters)

        operation_id = self.get_operation_id(operation_keys)
        summary, description = self.get_summary_and_description()
        security = self.get_security()
        assert security is None or isinstance(
            security, list
        ), "security must be a list of securiy requirement objects"
        deprecated = self.is_deprecated()
        tags = self.get_tags(operation_keys)

        responses = self.get_responses()

        operation = openapi.Operation(
            operation_id=operation_id,
            description=force_real_str(description),
            summary=force_real_str(summary),
            responses=responses,
            parameters=parameters,
            consumes=consumes,
            produces=produces,
            tags=tags,
            security=security,
            deprecated=deprecated,
        )
        return self.set_x_code_samples(operation)


class CustomTagAutoSchema(XCodeSampleAutoSchema):
    """This schema generator looks for the view tag name in its definition
    If none is found, fallback to default behavior
    """

    def get_tags(self, operation_keys=None):
        if getattr(self.view, "swagger_tags", None):
            return self.view.swagger_tags
        return super().get_tags(operation_keys)


class TaggedDescriptionSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)
        tags = {
            tag
            for path in swagger.paths.items()
            for op in path[1].operations
            for tag in op[1].tags
        }
        swagger.tags = [tag_extra_data.get(tag, {"name": tag}) for tag in tags]
        return swagger
