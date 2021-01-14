class WalletException(Exception):
    def __init__(self, wallet_id=None, *a, **kw):
        self.wallet_id = wallet_id
        super().__init__(*a, **kw)


class WalletNotFoundException(WalletException):
    pass


class OperationUnavailableException(WalletException):
    pass


class InsufficientFundsException(WalletException):
    pass


class IdenticalWalletsException(WalletException):
    pass
