from .Account import Account
from .EnumTypes import AccountType, AccountOwnerType, WithdrawOrderType

import logging

logger = logging.getLogger(__name__)


def WithdrawOrderType2List(withdrawOrder: WithdrawOrderType):
    """turns a WithdrawOrderType into a list of AccountTypes"""
    match withdrawOrder:
        case WithdrawOrderType.TaxDeferred_Regular_TaxFree:
            return [AccountType.TaxDeferred, AccountType.Regular, AccountType.TaxFree]
        case WithdrawOrderType.TaxDeferred_TaxFree_Regular:
            return [AccountType.TaxDeferred, AccountType.TaxFree, AccountType.Regular]
        case WithdrawOrderType.Regular_TaxFree_TaxDeferred:
            return [AccountType.Regular, AccountType.TaxFree, AccountType.TaxDeferred]
        case WithdrawOrderType.Regular_TaxDeferred_TaxFree:
            return [AccountType.Regular, AccountType.TaxDeferred, AccountType.TaxFree]
        case WithdrawOrderType.TaxFree_TaxDeferred_Regular:
            return [AccountType.TaxFree, AccountType.TaxDeferred, AccountType.Regular]
        case WithdrawOrderType.TaxFree_Regular_TaxDeferred:
            return [AccountType.TaxFree, AccountType.Regular, AccountType.TaxDeferred]
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

        assert isinstance(spouseAge, int)
        self.spouseAge = spouseAge

        assert isinstance(spouseIsAlive, bool)
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

        # now puts accounts into asset list based on withdrawOrder
        for _type in WithdrawOrderType2List(self.withdrawOrder):
            match _type:
                case AccountType.TaxDeferred:
                    self._assets += _taxdeferred
                case AccountType.Regular:
                    self._assets += _regular
                case AccountType.TaxFree:
                    self._assets += _taxfree

    def reconcile_required_withdraw(self, deficit: int):
        _dict = {}
        _dict[AccountType.TaxDeferred] = 0
        _dict[AccountType.TaxFree] = 0
        _dict[AccountType.Regular] = 0
        for _asset in self._assets:
            if _asset.Balance <= 0:
                continue
            if _asset.Type in (AccountType.TaxDeferred, AccountType.TaxFree):
                # need to check that owner is old enough to take withdraw
                # for now we assume that we cannot access these accounts if owner < 59 years of age
                match _asset.Owner:
                    case AccountOwnerType.Client:
                        if self.clientAge < 59:
                            continue
                    case AccountOwnerType.Spouse:
                        if self.spouseAge < 59:
                            continue

            # if we get here, we can take some money from the account..
            # need to look into how I can use the new account variables for Taxable income, etc
            # for these since I am taking money out of the accounts.
            # this may simplify the logic below somewhat..
            if deficit <= _asset.Balance:
                _dict[_asset.Type] += deficit
                _asset.Balance -= deficit
                logger.debug(
                    "taking %s from %s when client is %s, spouse is %s"
                    % (deficit, _asset.Name, self.clientAge, self.spouseAge)
                )
                return 0, _dict  # resulting deficit
            elif _asset.Balance > 0:  # deficit is greater than balance
                _dict[_asset.Type] += _asset.Balance
                deficit -= _asset.Balance
                _asset.Balance = 0
                logger.debug(
                    "taking total balance of %s from %s when client is %s, spouse is %s"
                    % (deficit, _asset.Name, self.clientAge, self.spouseAge)
                )

        return deficit, _dict
