from app.calculation import add
from app.calculation import BankAccount
import pytest

@pytest.mark.parametrize("num1, num2, result", [(1,2,3),(4,8,12), (9,0,9)])
def test_add(num1, num2, result):
    print('start testing')
    result = add(5, 4)
    assert result == 9



def test_bank_account_balence():
    Bank_account = BankAccount(50)
    assert Bank_account.balence == 50