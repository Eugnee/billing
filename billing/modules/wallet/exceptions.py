class WalletException(Exception):
    def __init__(self, wallet_id=None, *a) -> None:
        self.wallet_id = wallet_id
        super().__init__(*a)


class WalletNotFoundException(WalletException):
    pass


class OperationUnavailableException(WalletException):
    pass


class InsufficientFundsException(WalletException):
    pass


class IdenticalWalletsException(WalletException):
    pass
