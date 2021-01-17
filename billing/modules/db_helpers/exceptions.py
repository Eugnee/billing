class BaseEntityException(Exception):
    def __init__(self, entity: dict, *a) -> None:
        self.entity = entity
        super().__init__(*a)


class CreateEntityException(BaseEntityException):
    pass


class UpdateEntityException(BaseEntityException):
    pass
