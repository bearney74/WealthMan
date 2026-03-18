from .Account import Account
from .EnumTypes import AccountType, AccountOwnerType, WithdrawOrderType

import logging

logger = logging.getLogger(__name__)


def WithdrawOrderType2List(withdrawOrder: WithdrawOrderType):
    """turns a WithdrawOrderType into a list of AccountTypes"""
    match withdrawOrder:
        case WithdrawOrderType.TAXDEFERRED_REGULAR_TAXFREE:
            return [AccountType.TAXDEFERRED, AccountType.REGULAR, AccountType.TAXFREE]
        case WithdrawOrderType.TAXDEFERRED_TAXFREE_REGULAR:
            return [AccountType.TAXDEFERRED, AccountType.TAXFREE, AccountType.REGULAR]
        case WithdrawOrderType.REGULAR_TAXFREE_TAXDEFERRED:
            return [AccountType.REGULAR, AccountType.TAXFREE, AccountType.TAXDEFERRED]
        case WithdrawOrderType.REGULAR_TAXDEFERRED_TAXFREE:
            return [AccountType.REGULAR, AccountType.TAXDEFERRED, AccountType.TAXFREE]
        case WithdrawOrderType.TAXFREE_TAXDEFERRED_REGULAR:
            return [AccountType.TAXFREE, AccountType.TAXDEFERRED, AccountType.REGULAR]
        case WithdrawOrderType.TAXFREE_REGULAR_TAXDEFERRED:
            return [AccountType.TAXFREE, AccountType.REGULAR, AccountType.TAXDEFERRED]
        case _:
            logger.error("Invalid Withdraw Order Type '%s'" % withdrawOrder)


class WithdrawStrategy:
    def __init__(
        self,
        withdrawOrder: WithdrawOrderType,
        clientAge: int,
        clientIsAlive: bool,
        spouseAge: int,
        spouseIsAlive: bool,
        assets: [Account],
    ):

        assert isinstance(withdrawOrder, WithdrawOrderType)
        self.withdrawOrder = withdrawOrder

        assert isinstance(clientAge, int)
        self.clientAge = clientAge

        assert isinstance(clientIsAlive, bool)
        self.clientIsAlive = clientIsAlive

        assert isinstance(spouseIsAlive, bool)
        self.spouseIsAlive = spouseIsAlive

        if spouseIsAlive:
            assert isinstance(spouseAge, int)
            self.spouseAge = spouseAge
        else:
            self.spouseAge = None

        self._assets = []

        _REGULAR = []
        _TAXFREE = []
        _TAXDEFERRED = []

        for _asset in assets:
            match _asset.Type:
                case AccountType.REGULAR:
                    _REGULAR.append(_asset)
                case AccountType.TAXDEFERRED:
                    _TAXDEFERRED.append(_asset)
                case AccountType.TAXFREE:
                    _TAXFREE.append(_asset)
                case _:
                    logger.error("invalid asset type '%s'" % _asset.type)

        # now puts accounts into asset list based on withdrawOrder
        for _type in WithdrawOrderType2List(self.withdrawOrder):
            match _type:
                case AccountType.TAXDEFERRED:
                    self._assets += _TAXDEFERRED
                case AccountType.REGULAR:
                    self._assets += _REGULAR
                case AccountType.TAXFREE:
                    self._assets += _TAXFREE

    def reconcile_required_withdraw(self, deficit: int):
        _dict = {}
        _dict[AccountType.TAXDEFERRED] = 0
        _dict[AccountType.TAXFREE] = 0
        _dict[AccountType.REGULAR] = 0
        for _asset in self._assets:
            if _asset.balance <= 0:
                continue
            if _asset.Type in (AccountType.TAXDEFERRED, AccountType.TAXFREE):
                # need to check that owner is old enough to take withdraw
                # for now we assume that we cannot access these accounts if owner < 59 years of age
                match _asset.Owner:
                    case AccountOwnerType.CLIENT:
                        if self.clientAge < 59:
                            continue
                    case AccountOwnerType.SPOUSE:
                        if self.spouseAge < 59:
                            continue

            # if we get here, we can take some money from the account..
            # need to look into how I can use the new account variables for Taxable income, etc
            # for these since I am taking money out of the accounts.
            # this may simplify the logic below somewhat..
            if deficit <= _asset.balance:
                _dict[_asset.Type] += deficit
                _asset.withdraw(deficit)
                # _asset.Balance -= deficit
                logger.debug(
                    "taking %s from %s when client is %s, spouse is %s"
                    % (deficit, _asset.Name, self.clientAge, self.spouseAge)
                )
                return 0, _dict  # resulting deficit
            elif _asset.balance > 0:  # deficit is greater than balance
                _dict[_asset.Type] += _asset.balance
                deficit -= _asset.balance
                # print(_asset.balance)
                _asset.withdraw(_asset.balance)
                # _asset.Balance = 0
                logger.debug(
                    "taking total balance of %s from %s when client is %s, spouse is %s"
                    % (deficit, _asset.Name, self.clientAge, self.spouseAge)
                )

        return deficit, _dict
