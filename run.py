import gspread
from google.oauth2.service_account import Credentials

CREDS = Credentials.from_service_account_file("creds.json")
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# check api works with simple print statement of all values
# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)


def get_sales_data():
    """
    Get sales figures
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here:\n")
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError, if strings cannot be converted into int
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}")

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, sheetname):
    """
    Update <name> worksheet - adding new row from parameter provided
    """
    print(f"Updating {sheetname} worksheet...")
    the_worksheet = SHEET.worksheet(sheetname)
    the_worksheet.append_row(data)
    print(f"{sheetname} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figures subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made where stock was sold out.

    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    stock_row_int = [int(item) for item in stock_row]
    surplus_data = []

    for stock, sales in zip(stock_row_int, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from worksheet and returns the data as a list
    """
    sandwich_lists = []
    sales = SHEET.worksheet("sales")
    for col in range(1, 7):
        column = sales.col_values(col)
        sandwich_lists.append(column[-5:])
    return sandwich_lists


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    Returns one row
    """
    print("Calculating stock data...")
    new_stock_data = []
    for col in data:
        int_col = [int(num) for num in col]
        avg = sum(int_col)/len(int_col)
        new_stock_data.append(round(avg*1.1))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("\nWelcome to LoveSandwiches Data Automation\n")
main()

