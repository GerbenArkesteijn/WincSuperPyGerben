# Imports
import csv
import argparse
from datetime import datetime, timedelta

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main(args):
    inventory_temp = read_inventory(args.file)

    if args.advance_time:
        new_date = advance_time(args.advance_time)
        print(
            f"Time advanced by {args.advance_time} days. Current date: {new_date.strftime('%Y-%m-%d')}")
    elif args.buy:
        buy_item(inventory_temp, args.product_name,
                 args.buy_price, args.expiration_date)
        write_inventory(args.file, inventory_temp)
    elif args.sell:
        sell_item(inventory_temp, args.id, args.sell_price)
        write_inventory(args.file, inventory_temp)
    elif args.remove:
        remove_item(inventory_temp, args.id)
        write_inventory(args.file, inventory_temp)
    elif args.display:
        display_inventory(inventory_temp)
    elif args.report:
        if args.report_type == 'profit':
            generate_profit_report(inventory_temp, args.report_file)
        elif args.report_type == 'revenue':
            generate_revenue_report(inventory_temp, args.report_file)
        elif args.report_type == 'productsoverview':
            generate_products_overview_report(inventory_temp, args.report_file)
        elif args.report_type == 'inventory':
            generate_inventory_report(inventory_temp, args.report_file)
        elif args.report_type == 'purchase':
            generate_purchase_report(inventory_temp, args.report_file)
        elif args.report_type == 'sales':
            generate_sales_report(inventory_temp, args.report_file)
        else:
            print(
                "Invalid report type. Available report types: profit, revenue, productsoverview, inventory, purchase, sales")


def read_inventory(filename):
    inventory_temp = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            inventory_temp.append(row)
    return inventory_temp


def write_inventory(filename, inventory_temp):
    if len(inventory_temp) == 0:
        print("Inventory is empty. Nothing to write.")
    else:
        fieldnames = inventory_temp[0].keys()
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventory_temp)


def buy_item(inventory_temp, product_name, buy_price, expiration_date):
    product_name = input("Enter the product name of the item to buy: ")
    buy_price = input("Enter the price of the item to buy: ")
    expiration_date = input("Enter the expiration date of the item to buy: ")
    # Generate a unique 'id' for the item:
    # If the inventory is not empty (len(inventory) > 0), it retrieves the last item in the inventory and
    # gets the 'id' value of that item (last_item['id']). It then increments the 'id' by 1 to generate
    # a new unique 'id' for the item being added.

    # If the inventory is empty, it assigns the 'id' value of 1 for the first item.
    # The new item is created as a dictionary with the 'id' and the other keys.
    # The new item is appended to the inventory_temp list.
    # Each time the call buy_item() is used for registering a purchase,
    # it will automatically assign a unique 'id' to the item based on the already existing items in the inventory.
    if len(inventory_temp) > 0:
        last_item = inventory_temp[-1]
        last_id = last_item['id']
        id = int(last_id) + 1
    else:
        id = 1
    # set the buy_date
    buy_date = get_current_date()
    sell_price = None
    sell_date = None

    # Create the new item dictionary
    item = {'id': id, 'product_name': product_name, 'buy_price': buy_price,
            'buy_date': buy_date, 'sell_price': sell_price,
            'sell_date': sell_date, 'expiration_date': expiration_date}
    # Add the item to the inventory
    inventory_temp.append(item)
    print("Purchased item is successfully added.")


def remove_item(inventory_temp, id):
    id = input("Enter the id of the item to remove: ")
    for item in inventory_temp:
        if item['id'] == id:
            inventory_temp.remove(item)
            print("Item removed successfully.")


def sell_item(inventory_temp, id, sell_price):
    id = input("Enter the id of the item to sell: ")
    item_found = False
    for item in inventory_temp:
        if item['id'] == id:
            item_found = True
            if item['sell_price'] == "":
                # Set the 'sell_date'
                item['sell_date'] = get_current_date()
                item['sell_price'] = input(
                    "Enter the price of the item to sell: ")
                return print("Sold item successfully")
            else:
                print("The item with this id is already sold.")

    if item_found is False:
        return print("Item id not found")


def display_inventory(inventory_temp):
    print("Inventory:")
    for item in inventory_temp:
        print(f"id: {item['id']}, product_name: {item['product_name']}, buy_price: {item['buy_price']}, buy_date: {item['buy_date']}, sell_price: {item['sell_price']}, sell_date: {item['sell_date']}, expiration_date: {item['expiration_date']}")


# Function to report products overview
def generate_products_overview_report(inventory_temp, report_file):
    unique_products = set()

    for item in inventory_temp:

        if item['sell_price'] == "":
            unique_products.add(item['product_name'])

    print("Unique Products")
    print("----------------")
    print(unique_products)

    # Write the product overview report to the CSV file
    with open(report_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for product in unique_products:
            writer.writerow([product])

    print(f"Product overview has been written to '{report_file}'.")


# Function to report how many of each type of product the supermarket holds currently;
def generate_inventory_report(inventory_temp, report_file):
    products_all = []
    today = get_current_date()

    for item in inventory_temp:

        if item['sell_price'] == "" and item['expiration_date'] > today:
            products_all.append(item['product_name'])
            print(item)

    products_all_new = sorted(products_all)

    print("Inventory")
    print("----------------")
    print(products_all_new)

    # count the occurences of each product in the list
    inventory_report = []

    for product in products_all_new:
        quantity = products_all_new.count(product)
        tuple = (product, quantity)
        print("Tuple has:")
        print(tuple)

        inventory_report.append(tuple)

    # remove duplicate tuples
    inventory_report_set = set(inventory_report)

    print("Inventory Report")
    print("-------------")
    print(inventory_report_set)

    # write output to csv file
    fieldnames = ['Product', 'Quantity']
    with open(report_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer = csv.writer(csvfile)
        for row in inventory_report_set:
            writer.writerow(row)
        print(f"Inventory report has been written to '{report_file}'.")


# Function to report how much each product was bought for, and what its expiry date is
def generate_purchase_report(inventory_temp, report_file):
    purchases = []
    for item in inventory_temp:
        purchases.append((item['id'], item['product_name'],
                         item['buy_price'], item['expiration_date']))

    print("Purchase Report")
    print("-------------")
    print(purchases)

    fieldnames = ['Id', 'Product', 'Buy price', 'Expiration date']
    with open(report_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer = csv.writer(csvfile)
        for row in purchases:
            writer.writerow(row)
        print(f"Purchase report has been written to '{report_file}'.")


# Function to report how much each product was sold for or if it expired, the fact that it did
def generate_sales_report(inventory_temp, report_file):
    sales = []
    today = get_current_date()

    for item in inventory_temp:
        if item['expiration_date'] < today:
            sales.append((item['id'], item['product_name'],
                         item['sell_price'], item['expiration_date'], 'yes'))
        elif item['sell_price'] and item['expiration_date'] >= today:
            sales.append((item['id'], item['product_name'],
                         item['sell_price'], item['expiration_date'], 'no'))

    print("Sales Report")
    print("-------------")
    print(sales)

    fieldnames = ['Id', 'Product', 'Sell price', 'Expiration date', 'Expired']
    with open(report_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer = csv.writer(csvfile)
        for row in sales:
            writer.writerow(row)
        print(f"Sales report has been written to '{report_file}'.")


# Function to report profit
def generate_profit_report(inventory_temp, report_file):
    total_profit = 0
    today = get_current_date

    # Calculate profit for each item and accumulate the total profit
    for item in inventory_temp:

        sell_price = item['sell_price']
        cost_price = float(item['buy_price'])

        # if sell_price:
        if sell_price and sell_price <= today:
            # 'sell_price' is not empty, so calculate profit
            sell_price = float(sell_price)
            profit = (sell_price - cost_price)
            total_profit += profit

    print("Profit Report")
    print("-------------")
    print("Total Profit: $", total_profit)

    # Write the profit report to the CSV file
    with open(report_file, 'w', newline='') as csvfile:
        fieldnames = ['Total Profit']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Total Profit': total_profit})

    print(f"Profit report has been written to '{report_file}'.")


# Function to report revenue
def generate_revenue_report(inventory_temp, report_file):
    total_revenue = 0
    today = get_current_date()

    # Calculate profit for each item and accumulate the total profit
    for item in inventory_temp:

        sell_price = item['sell_price']

        # if sell_price:
        if sell_price and sell_price <= today:
            # 'sell_price' is not empty, so calculate profit
            sell_price = float(sell_price)
            revenue = sell_price
            total_revenue += revenue

    print("Revenue Report")
    print("-------------")
    print("Total Revenue: $", total_revenue)

    # Write the profit report to the CSV file
    with open(report_file, 'w', newline='') as csvfile:
        fieldnames = ['Total Revenue']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Total Revenue': total_revenue})

    print(f"Revenue report has been written to '{report_file}'.")

    # Function to set and save the current date to a file
    def set_current_date(date=None):
        if date is None:
            date = datetime.now()  # Get today's date and time
        with open("current_date.txt", "w") as file:
            file.write(date.strftime("%Y-%m-%d"))

    # Function to read the current date
    def get_current_date():
        with open("current_date.txt", "r") as file:
            date_str = file.readline().strip()
            return date_str

    # Function to advance the current date by a specified number of days
    def advance_time(days_to_advance):
        current_date = get_current_date()
        new_date = datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=days_to_advance)
        set_current_date(new_date)
        return new_date


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inventory Management System')
    parser.add_argument('file', help='CSV file to store inventory data')
    parser.add_argument('-b', '--buy', action='store_true', help='Buy an item')
    parser.add_argument('-r', '--remove', action='store_true',
                        help='Remove an item from inventory')
    parser.add_argument('-s', '--sell', action='store_true',
                        help='Sell an item')
    parser.add_argument('-d', '--display',
                        action='store_true', help='Display inventory')
    parser.add_argument('--product_name', help='Product name of the item')
    parser.add_argument('--buy_price', type=float,
                        help='Buy_price of the item')
    parser.add_argument('--sell_price', type=float,
                        help='Sell_price of the item')
    parser.add_argument('--id', type=float, help='Id of the item')
    parser.add_argument('--expiration_date',
                        help='Expiration date of the item')
    parser.add_argument('--report', action='store_true',
                        help='Generate a report')
    parser.add_argument('--report_type', choices=['profit', 'revenue',
                        'productsoverview', 'inventory', 'purchase', 'sales'], help='Type of report to generate')
    parser.add_argument('--report_file', default='report.csv',
                        help='Filename for the generated report')
    parser.add_argument("--advance-time", type=int,
                        help="Advance time by a specified number of days")

    args = parser.parse_args()
    main(args)
