from tortoise import models, fields


class Config(models.Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=64, unique=True)
    value = fields.TextField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Weather(models.Model):
    id = fields.IntField(pk=True)
    to = fields.CharField(max_length=64)
    is_room = fields.BooleanField()
    adcode = fields.CharField(max_length=32)
    at_hour = fields.IntField(default=0)
    address = fields.CharField(max_length=128)
    type = fields.CharField(max_length=32)
    error = fields.IntField(default=0)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        unique_together = (("to", "is_room", "adcode"),)
