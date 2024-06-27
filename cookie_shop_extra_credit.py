import csv

def bake_cookies(filepath):
    cookies = []
    with open(filepath, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cookie = {
                'id': int(row['id']),
                'title': row['title'],
                'description': row['description'],
                'price': float(row['price'].replace('$', '').strip()),
                'sugar_free': row['sugar_free'].lower() == 'true',
                'gluten_free': row['gluten_free'].lower() == 'true',
                'contains_nuts': row['contains_nuts'].lower() == 'true'
            }
            cookies.append(cookie)
    return cookies
def welcome():
    print("Welcome to the Python Cookie Shop!")
    print("We feed each according to their need.")

def get_dietary_restrictions():
    print("\nWe'd hate to trigger an allergic reaction in your body. So please answer the following questions:")
    nuts = input("Are you allergic to nuts? ").strip().lower() in ['yes', 'y']
    gluten = input("Are you allergic to gluten? ").strip().lower() in ['yes', 'y']
    sugar = input("Do you suffer from diabetes? ").strip().lower() in ['yes', 'y']
    return {'nuts': nuts, 'gluten': gluten, 'sugar': sugar}

def filter_cookies(cookies, restrictions):
    filtered_cookies = []
    for cookie in cookies:
        if restrictions['nuts'] and cookie['contains_nuts']:
            continue
        if restrictions['gluten'] and not cookie['gluten_free']:
            continue
        if restrictions['sugar'] and not cookie['sugar_free']:
            continue
        filtered_cookies.append(cookie)
    return filtered_cookies

def display_cookies(cookies):
    print("Here are the cookies we have in the shop for you:\n")
    for cookie in cookies:
        print(f"#{cookie['id']} - {cookie['title']}")
        print(f"{cookie['description']}")
        print(f"Price: ${cookie['price']:.2f}\n")

def get_cookie_from_dict(id, cookies):
    for cookie in cookies:
        if cookie['id'] == id:
            return cookie
    return None

def solicit_quantity(id, cookies):
    cookie = get_cookie_from_dict(id, cookies)
    while True:
        try:
            quantity = int(input(f"My favorite! How many {cookie['title']} would you like? "))
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
            subtotal = quantity * cookie['price']
            print(f"Your subtotal for {quantity} {cookie['title']} is ${subtotal:.2f}.")
            return quantity
        except ValueError:
            print("Please enter a valid number.")
    
def solicit_order(cookies):
    orders = []
    while True:
        id_input = input('Enter the number of any cookie you would like to purchase (type "finished" if finished with your order): ').strip().lower()
        if id_input in ['finished', 'done', 'quit', 'exit']:
            break
        try:
            id = int(id_input)
            if get_cookie_from_dict(id, cookies) is None:
                raise ValueError("Invalid cookie ID.")
            quantity = solicit_quantity(id, cookies)
            orders.append({'id': id, 'quantity': quantity})
        except ValueError:
            print("Please enter a valid cookie ID.")
    return orders

def display_order_total(order, cookies):
    total = 0
    print("\nThank you for your order. You have ordered:")
    for item in order:
        cookie = get_cookie_from_dict(item['id'], cookies)
        quantity = item['quantity']
        subtotal = quantity * cookie['price']
        total += subtotal
        print(f"-{quantity} {cookie['title']}")
    print(f"\nYour total is ${total:.2f}.")
    print("Please pay with Bitcoin before picking-up.\n")
    print("Thank you!")
    print("-The Python Cookie Shop Robot.")

def run_shop(cookies):
    welcome()
    restrictions = get_dietary_restrictions()
    filtered_cookies = filter_cookies(cookies, restrictions)
    display_cookies(filtered_cookies)
    order = solicit_order(filtered_cookies)
    display_order_total(order, cookies)

