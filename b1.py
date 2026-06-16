class BankAccount:
    bank_name = "Vietcombank"
    transaction_fee = 2000

    def __init__(self, account_number: str, account_name: str):
        self.account_number = account_number
        self._account_name = None
        self.account_name = account_name
        self.__balance = 0
    @property
    def balance(self):
        return self.__balance
    @property
    def account_name(self):
        return self._account_name
    @account_name.setter
    def account_name(self, name):
        normalized_name = " ".join(str(name).split())
        if not normalized_name:
            print("Tên tài khoản không được để trống")
            return
        self._account_name = normalized_name.upper()

    @staticmethod
    def validate_account_number(account_number):
        if not account_number.isdigit() or len(account_number) != 10:
            return False
        return True

    @classmethod
    def update_transaction_fee(cls, new_fee: int):
        if new_fee < 0:
            print("Phí giao dịch không được âm")
            return False
        cls.transaction_fee = new_fee
        return True

    def deposit(self, amount: int):
        if amount <= 0:
            print("Số tiền giao dịch phải lớn hơn 0")
            return False
        self.__balance += amount
        return True

    def withdraw(self, amount: int):
        if amount <= 0:
            print("Số tiền giao dịch phải lớn hơn 0")
            return False
        total = amount + BankAccount.transaction_fee
        if self.__balance < total:
            print("Giao dịch thất bại. Số dư không đủ để thanh toán số tiền và phí giao dịch")
            return False
        self.__balance -= total
        return True

    def display_info(self):
        print("--- THÔNG TIN TÀI KHOẢN ---")
        print(f"Ngân hàng: {BankAccount.bank_name}")
        print(f"Số tài khoản: {self.account_number}")
        print(f"Tên chủ tài khoản: {self.account_name}")
        print(f"Số dư hiện tại: {self.balance:,} VND")
        print(f"Phí giao dịch: {BankAccount.transaction_fee:,} VND")


def format_money(value: int) -> str:
    return f"{value:,}"

def require_account(account):
    if account is None:
        print("Hệ thống chưa có thông tin tài khoản")
        print("Vui lòng mở tài khoản ở Chức năng 1 trước.")
        return False
    return True

def read_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        return None


def open_account():
    print("--- MỞ TÀI KHOẢN MỚI ---")
    while True:
        account_number = input("Nhập số tài khoản 10 chữ số: ").strip()
        if BankAccount.validate_account_number(account_number):
            break
        print("Số tài khoản không hợp lệ!")
        print("Số tài khoản phải gồm đúng 10 chữ số.")

    while True:
        account_name = input("Nhập tên chủ tài khoản: ")
        normalized_name = " ".join(account_name.split())
        if normalized_name:
            return BankAccount(account_number, normalized_name)
        print("Tên tài khoản không được để trống")


def transaction_menu(account):
    print("--- GIAO DỊCH NẠP / RÚT TIỀN ---")
    print("1. Nạp tiền")
    print("2. Rút tiền")
    action = input("Chọn loại giao dịch (1-2): ").strip()
    if action not in {"1", "2"}:
        print("Chọn loại giao dịch không hợp lệ")
        return

    amount = read_int("Nhập số tiền giao dịch: ")
    if amount is None:
        print("Vui lòng nhập số hợp lệ")
        return

    if action == "1":
        if account.deposit(amount):
            print(f"Nạp tiền thành công: +{format_money(amount)} VND")
    else:
        if account.withdraw(amount):
            print(f"Rút tiền thành công: -{format_money(amount)} VND")
            print(f"Phí giao dịch: {format_money(BankAccount.transaction_fee)} VND")

    print(f"Số dư mới: {format_money(account.balance)} VND")


def update_account_name(account):
    print("--- CẬP NHẬT TÊN CHỦ TÀI KHOẢN ---")
    new_name = input("Nhập tên mới: ")
    old_name = account.account_name
    account.account_name = new_name
    if account.account_name != old_name:
        print(f"Cập nhật thành công. Tên mới: {account.account_name}")


def update_fee():
    print("--- ĐỔI PHÍ GIAO DỊCH HỆ THỐNG ---")
    print(f"Phí giao dịch hiện tại: {format_money(BankAccount.transaction_fee)} VND")
    fee = read_int("Nhập phí giao dịch mới: ")
    if fee is None:
        print("Phí giao dịch không hợp lệ")
        return
    if BankAccount.update_transaction_fee(fee):
        print(f"Đã cập nhật phí giao dịch toàn hệ thống thành {format_money(BankAccount.transaction_fee)} VND")
    else:
        print(f"Phí giao dịch hiện tại vẫn là {format_money(BankAccount.transaction_fee)} VND")


def main():
    current_account = None
    while True:
        print("""
===== VIETCOMBANK DIGIBANK SIMULATOR =====
1. Mở tài khoản mới
2. Xem thông tin tài khoản
3. Giao dịch Nạp / Rút tiền
4. Cập nhật Tên chủ tài khoản
5. Đổi phí giao dịch hệ thống
6. Thoát chương trình
==========================================
""")
        choice = input("Chọn chức năng (1-6): ").strip()

        if choice == "1":
            current_account = open_account()
            print("Mở tài khoản thành công!")
            print(f"Số tài khoản: {current_account.account_number}")
            print(f"Tên chủ tài khoản: {current_account.account_name}")

        elif choice == "2":
            if require_account(current_account):
                current_account.display_info()

        elif choice == "3":
            if require_account(current_account):
                transaction_menu(current_account)

        elif choice == "4":
            if require_account(current_account):
                update_account_name(current_account)

        elif choice == "5":
            update_fee()

        elif choice == "6":
            print("Cảm ơn bạn đã sử dụng Vietcombank Digibank!")
            break

        else:
            print("Vui lòng chọn từ 1–6")


if __name__ == "__main__":
    main()
