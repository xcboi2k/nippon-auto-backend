from .constants import ENGINE_TYPES

ENGINE_TYPE_CHOICES = [(item["key"], item["label"]) for item in ENGINE_TYPES]

engine_type = models.CharField(
    max_length=30,
    choices=ENGINE_TYPE_CHOICES
)
