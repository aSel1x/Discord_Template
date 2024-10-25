from app.core.exception.base import RequestInvalid


class NotEnoughBalance(RequestInvalid):
    def __init__(self):
        super().__init__('Not enough balance')
