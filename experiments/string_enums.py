from enum import StrEnum
# from strenum import StrEnum


class DataItem:
    def __init__(
        self, header: str, format: str = "${:,}", default_data: [float, int] = 0
    ):
        self._header = header
        self._format = format
        self._data = default_data

    @property
    def header(self):
        return self._header

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def __str__(self):
        return self._format.format(self._data)


class WithdrawOrderType(StrEnum):
    TAXDEFERRED_REGULAR_TAXFREE = "Tax Deferred, Regular, Tax Free"
    TAXDEFERRED_TAXFREE_REGULAR = "Tax Deferred, Tax Free, Regular"
    REGULAR_TAXFREE_TAXDEFERRED = "Regular, Tax Free, Tax Deferred"
    REGULAR_TAXDEFERRED_TAXFREE = "Regular, Tax Deferred, Tax Free"
    TAXFREE_TAXDEFERRED_REGULAR = "Tax Free, Tax Deferred, Regular"
    TAXFREE_REGULAR_TAXDEFERRED = "Tax Free, Regular, Tax Deferred"


assert (
    WithdrawOrderType.TAXDEFERRED_REGULAR_TAXFREE == "Tax Deferred, Regular, Tax Free"
)

_d = DataItem("my cell", "{.value}", WithdrawOrderType.TAXDEFERRED_REGULAR_TAXFREE)
print(str(_d))

print(WithdrawOrderType["Tax Deferred, Regular, Tax Free"])
