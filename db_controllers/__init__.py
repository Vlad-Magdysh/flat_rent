"""
trick: it will contain mapping and use Config to select current database controller
"""
from typing import Type
from .base_controller import BaseController
from .mongodb_controller import MongoController

REGISTERED_CONTROLLERS = {
    MongoController.__name__: MongoController,
}


def get_current_controller_class(controller_name: str) -> Type[BaseController]:
    """
    Returns a child class of the BaseController.
    If controller_name does not exist - return MongoController
    """
    return REGISTERED_CONTROLLERS.get(controller_name, MongoController)
