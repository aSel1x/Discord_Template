from .base import NotFoundException


class NotFound(NotFoundException):
    def __init__(self):
        super().__init__('User not found')
