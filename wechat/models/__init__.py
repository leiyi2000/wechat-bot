from tortoise import models, fields


class Config(models.Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=64, unique=True)
    value = fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
