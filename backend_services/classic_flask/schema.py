from marshmallow import fields, Schema, ValidationError, validate

USD = "USD"
UAH = "UAH"


class CustomSchema(Schema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all attribute names accessible by .name annotation. To avoid hardcoded keys, like dict_1["abracadabra"]
        for attr_name in self._declared_fields.keys():
            setattr(self, attr_name, attr_name)


class GetFlatsSchema(CustomSchema):
    page_number = fields.Int(required=False, load_default=0)
    lower_price = fields.Int(required=False)
    upper_price = fields.Int(required=False)
    currency = fields.String(required=False, validate=validate.OneOf((UAH, USD)), load_default=UAH)
    square = fields.Int(required=False)
    rooms = fields.Int(required=False, validate=lambda n: n > 0, error='Value must be greater than zero.')
    tags = fields.List(fields.String(), required=False)
    locations = fields.List(fields.String(), required=False)
    new = fields.Bool(required=False, load_default=False)


def extract_arguments(schema: Schema, request) -> dict:
    """
    Extracts arguments from a Flask request based on a Marshmallow schema.

    Args:
        schema: Marshmallow schema for the request arguments.
        request: A Flask request object with the parameters
    Returns:
        Dict containing the validated request arguments.

    Raises:
        ValidationError: If the request arguments fail validation against the schema.
    """
    # Get the request arguments from the appropriate location (query string, form data, or JSON)
    args = request.args if request.method == "GET" else request.get_json() or request.form

    # Use Marshmallow to validate and deserialize the arguments
    try:
        validated_args = schema.load(args)
    except ValidationError as e:
        # Reraise the validation error with a 400 status code
        raise ValidationError(str(e), status_code=400)

    return validated_args
