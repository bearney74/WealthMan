from .Account import Account
from .EnumTypes import AccountType, AccountOwnerType

import logging

logger = logging.getLogger(__name__)


class WithdrawStrategy:
    def __init__(
        self,
        withdrawOrder,
        clientAge: int,
        clientIsAlive: bool,
        spouseAge: int,
        spouseIsAlive: bool,
        assets: [Account],
    ):
        assert withdrawOrder in [
            "TaxDeferred,Regular,TaxFree",
            "TaxDeferred,TaxFree,Regular",
            "Regular,TaxFree,TaxDeferred",
            "Regular,TaxDeferred,TaxFree",
            "TaxFree, TaxDeferred,Regular",
            "TaxFree,Regular,TaxDeferred",
        ]

        self.withdrawOrder = withdrawOrder
        self.clientAge = clientAge
        self.clientIsAlive = clientIsAlive
        self.spouseAge = spouseAge
        self.spouseIsAlive = spouseIsAlive
        self._assets = []

        _regular = []
        _taxfree = []
        _taxdeferred = []

        for _asset in assets:
            match _asset.Type:
                case AccountType.Regular:
                    _regular.append(_asset)
                case AccountType.TaxDeferred:
                    _taxdeferred.append(_asset)
                case AccountType.TaxFree:
                    _taxfree.append(_asset)
                case _:
                    logger.error("invalid asset type '%s'" % _asset.type)

        # now set assets variable based on withdrawOrder
        _list = self.withdrawOrder.split(",")
        for _type in self.withdrawOrder.split(","):
            match _type:
                case "TaxDeferred":
                    self._assets += _taxdeferred
                case "Regular":
                    self._assets += _regular
                case "TaxFree":
                    self._assets += _taxfree
                case _:
                    logger.error("invalid asset type '%s'" % _type)

    def reconcile_required_withdraw(self, deficit: int):
        for _asset in self._assets:
            assert _asset.Balance >= 0
            if _asset.Type in (AccountType.TaxDeferred, AccountType.TaxFree):
                # need to check that owner is old enough to take withdraw
                match _asset.Owner:
                    case AccountOwnerType.Client:
                        if self.clientAge < 59:
                            continue
                    case AccountOwnerType.Spouse:
                        if self.spouseAge < 59:
                            continue
            # if we get here, we can take some money from the account..
            if deficit <= _asset.Balance:
                _asset.Balance -= deficit
                logger.debug(
                    "taking %s from %s when client is %s, spouse is %s"
                    % (deficit, _asset.Name, self.clientAge, self.spouseAge)
                )
                return 0  # resulting deficit
            else:  # deficit is greater than balance
                deficit -= _asset.Balance
                _asset.Balance = 0
                logger.debug(
                    "taking total balance of %s from %s when client is %s, spouse is %s"
                    % (deficit, _asset.Name, self.clientAge, self.spouseAge)
                )

        return deficit
