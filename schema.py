from marshmallow import Schema, fields

class ItemRequest(Schema):
    i_title = fields.String(required=True, description="What item do you want?")

class ItemResponse(Schema):
    i_title = fields.String(default="Success")

# class EmailWatchRequest(Schema):
#     headers = fields.Mapping()

# class EmailWatchResponse(Schema):
#     headers = fields.Mapping()