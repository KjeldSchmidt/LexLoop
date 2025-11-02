from sqlalchemy.orm import declarative_base

Base = declarative_base()

# class MetaBase:
#     host = "http://localhost:7894"
#     region = "eu-central-1"
#     aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "fake")
#     aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "fake")
#     table_name_suffix = os.environ.get("ENV", "local")
#
#
# class ModelBase(Model):
#     class Meta(MetaBase):
#         abstract = True
#         table_name = "model_base"
#
#     def __init_subclass__(cls, **kwargs: dict[str, Any]) -> None:  # type: ignore[explicit-any]
#         super().__init_subclass__(**kwargs)
#         if not getattr(cls.Meta, "abstract", False):
#             cls.Meta.table_name = (
#                 cls.Meta.table_name + cls.Meta.table_name_suffix
#             )
