import json


class ProductManager:
    
    """
    
    This class handles the following functionality:
    
    - Add a product or increase its quantity (in case the product was already in stock)
    
    - Selling a product
    
    - Show products list in stock
    
    - Show net/gross profits
    
    """
    
    def __init__(self,product_name: str,product_quantity: int,purchase_price: float,
                 sell_price: float,product_to_sell: str,quantity_sold: int):
        
        self.product_name = product_name
        self.product_quantity = product_quantity
        self.purchase_price = purchase_price
        self.sell_price = sell_price
        self.product_to_sell = product_to_sell
        self.quantity_sold = quantity_sold

        """
        This method provides to add a new product or increment the quantity of an existing product in stock,
        save the information about the product in an external file.
        
        The information saved are:
        
        - Product name (str)
        - Quantity (int)
        - Purchase price (float)
        - Selling price (float)
        - Increments (quantity/purchase price) (floats)
        
        * About purchase price: you can never know if the price will change from the first purchase to
          subsequent purchases, after all inflation and deflation are real problems :).
          
        """
        
    def add_product(self):
        
        try:
            with open("inventory.json", 'r') as storage:
                inventory = json.load(storage)
        except (FileNotFoundError, json.JSONDecodeError):
            inventory = {}
             
        if self.product_name in inventory:
            print(f"The product '{self.product_name}' is already present in the inventory.")
            choice = input("Do you want to add increments to the existing product? (Y/N): ")
            if choice.lower() == "y":
                try:
                    quantity_increment = int(input("Enter the quantity increment: "))
                    if quantity_increment < 0:
                        raise ValueError("Quantity increment cannot be negative.")
                    
                    purchase_price_variation = float(input("Enter the purchase price increment: "))
                    if purchase_price_variation < 0:
                        raise ValueError("Purchase price cannot be negative")
                except ValueError as e:
                    print(f"Invalid input for increment: {str(e)}")
                    return
            
                inventory[self.product_name]['quantity'] += quantity_increment
                inventory[self.product_name]['purchase price'] += purchase_price_variation
                print("Increments added to the existing product.")
            else:
                print("No increments added. Existing product remains unchanged.")
        else:
            inventory[self.product_name] = {
                'purchase price': self.purchase_price,
                'quantity': self.product_quantity,
                'sell price': self.sell_price}

        with open("inventory.json", 'w') as storage:
            json.dump(inventory, storage, indent=4)

        print(f"ADDED: {self.product_quantity} X {self.product_name}")
     

    def list_products(self):
        
        """
        
        Lists the products and their details from the inventory.
        If the inventory is empty or has not been created, the program show warning messages.

        """
    
        try:
            with open("inventory.json", 'r') as storage:
                inventory = json.load(storage)
        except (FileNotFoundError, json.JSONDecodeError):
            print("The inventory has not been created or is empty.")
            return

        if inventory is None:
            print("The inventory is empty.")
            return
        
        column_widths = [40, 20, 10,10]

        print(f"{'Product name':<{column_widths[0]}} {'Quantity':<{column_widths[1]}} {'Price':>{column_widths[2]}}")

        print('-' * sum(column_widths))

        for product_name, product_details in inventory.items():
            print(f"{product_name:<{column_widths[0]}} {str(product_details['quantity']):<{column_widths[1]}} {str(product_details['sell price']):>{column_widths[2]}}$")


    def sell_product(self):
        
        """
        
        Handles the process of selling a product.
        This method checks the inventory file for the availability of the product to be sold and the requested quantity.
        If the product and requested quantity are available, it updates the inventory and sales record files accordingly.
        If the inventory file or sales record file does not exist or is empty/corrupted, where showed errors messages.
        
        """
        
        try:
            with open("inventory.json", 'r') as storage:
                inventory = json.load(storage)
        except FileNotFoundError:
            print("The inventory file does not exist.")
            return
        except json.JSONDecodeError:
            print("The inventory file is empty or corrupted.")
            return
        
        
        try:
            with open("sales_record.json", 'r') as sales:
                sales_record = json.load(sales)
        except (FileNotFoundError, json.JSONDecodeError):
            sales_record = {}


        if self.product_to_sell in inventory:
            available_quantity = inventory[self.product_to_sell]['quantity']
            if self.quantity_sold <= available_quantity:
                inventory[self.product_to_sell]['quantity'] -= self.quantity_sold
                
                if self.product_to_sell in sales_record:
                    sales_record[self.product_to_sell]['quantity sold'] += self.quantity_sold
                else:
                    sales_record[self.product_to_sell] = {
                    'purchase price': inventory[self.product_to_sell]['purchase price'],
                    'quantity sold': self.quantity_sold,
                    'sell price': inventory[self.product_to_sell]['sell price']
                    }
                    
                sell_price = inventory[self.product_to_sell]['sell price']  
                   
                print(f"Just sell {self.quantity_sold} unities of product: '{self.product_to_sell}'.")
                print("New quantity available:", inventory[self.product_to_sell]['quantity'])
            
                
                if inventory[self.product_to_sell]['quantity'] == 0:
                    del inventory[self.product_to_sell]
                    print("Since the product is out of stock, it has been removed from the inventory")
                    
                with open("inventory.json", 'w') as storage, open("sales_record.json", 'w') as sales:
                    json.dump(inventory, storage, indent=4)
                    json.dump(sales_record,sales,indent=4)
                
                return sell_price 
                  
            else:
                print("You cannot sell more products than you have in stock")
        else:
            print("The product does not exist in stock.")  
                        
    def calculate_profit(self):
        
        """
        Calculates the gross profit and net profit from the sales record.
        If the sales record file does not exist or is empty, Show an error message.
        
        Returns:
        gross_profit (float): The total gross profit.
        net_profit (float): The total net profit.

        """
        
        try:
            with open("sales_record.json", 'r') as sales:
                sales_record = json.load(sales)
        except (FileNotFoundError,json.JSONDecodeError):
            print("The sales record file does not exist or is empty.")
            return
        
        gross_profit = 0.0
        net_profit = 0.0

        for product_name, product_details in sales_record.items():
            quantity_sold = product_details['quantity sold']
            cost_price = product_details['purchase price'] * quantity_sold
            gross = product_details['sell price'] * quantity_sold
            net = gross - cost_price

            gross_profit += gross
            net_profit += net
            

        print("Profit Calculation:")
        print("-------------------")
        print(f"Gross Profit: {gross_profit}$")
        print(f"Net Profit: {net_profit}$")
          
        return gross_profit, net_profit

class UserInterface:
    """
    Represents the user interface for interacting with the product management system.

    This class provides a command-line interface for users to interact with the product management system. It displays a
    welcome message, shows a menu of available options, and handles user input to perform various operations such as
    adding a product, listing all products, recording a sale, showing net/gross profits, and quitting the program.

    Attributes:
        shop: An instance of the ProductManager class representing the product management system.

    Methods:
        start: Starts the user interface by displaying the welcome message and showing the menu.
        display_welcome_message: Displays a welcome message with ASCII art.
        show_menu: Displays the menu options and handles user input to perform the corresponding operations.
        display_menu_help: Displays the menu options to assist users in understanding the available choices.
        add_product: Handles the process of adding a new product to the system.
        list_products: Displays a list of all products in stock.
        sell_product: Handles the process of recording a product sale.
        calculate_profit: Calculates and displays the net and gross profits from recorded sales.
        
        """
    
    def __init__(self):
        self.shop = None

    def start(self):
        self.display_welcome_message()
        self.show_menu()

    def display_welcome_message(self):
        welcome_art = '''
                            __          ________ _      _____ ____  __  __ ______ 
                            \ \        / /  ____| |    / ____/ __ \|  \/  |  ____|
                             \ \  /\  / /| |__  | |   | |   | |  | | \  / | |__   
                              \ \/  \/ / |  __| | |   | |   | |  | | |\/| |  __|  
                               \  /\  /  | |____| |___| |___| |__| | |  | | |____ 
                                \/  \/   |______|______\_____\____/|_|  |_|______|
     
               type in the field below the command associated with the operation you intend to perform!
         
                                        (type help if you need the menu)
     
     
                                            add  ->   Add a product
                                           list  ->   List all products
                                           sell  ->   Record a sell
                                        profits  ->   Show profits
                                           quit  ->   Quit
                                                    
'''
        
        print(welcome_art)

    def show_menu(self):
        while True:
            
            options = {"add":"add a product",
                       "list":"list all products",
                       "sell":"record a sell",
                       "profits":"Show net/gross profits",
                       "quit":"Quit"}

            choice = input("Enter a command: ")
            
            if choice == "help":
                for k,v in options.items():  
                    print(f"{k}:{v}")
            
            if choice == "add":
                self.add_product()
            elif choice == "list":
                self.list_products()
            elif choice == "sell":
                self.sell_product()
            elif choice == "profits":
                self.calculate_profit()
            elif choice == "quit":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. available options are:")
                for k,v in options.items():  
                    print(f"{k}:{v}")
                

    def add_product(self):
        
        flag = True
        
        try:
            product_name = input("Enter the product name: ")
            
            while flag:
                product_quantity = int(input("Enter the product quantity: "))  
                purchase_price = float(input("Enter the purchase price: "))
                sell_price = float(input("Enter the sell price: "))
                
                if product_quantity < 0 or purchase_price < 0 or sell_price < 0:
                    print("Value(s) cannot be negative")
                    continue
                else:
                    flag = False
            
            self.shop = ProductManager(
                product_name,
                product_quantity,
                purchase_price,
                sell_price,
                product_to_sell=None,
                quantity_sold=None)
            self.shop.add_product()
        except (ValueError):
            print("Quantity value must be integer")
        except(UnboundLocalError):
            print("An error occurred")
        
    def list_products(self):
        self.shop = ProductManager("", 0, 0.0, 0.0, "", 0)
        self.shop.list_products()
        
                
    def sell_product(self):
        
        sells = []
        
        flag = True
        
        try:
            while flag:
                product_to_sell = input("Enter the product to sell: ")
                
                quantity_sold = int(input("Enter the quantity to sell: "))
                if type(quantity_sold) != int:
                    print("Invalid value. quantity sold must be an integer.")
                    continue
                if quantity_sold < 0:
                    print("Quantity sold cannot be negative")
                    continue
                    
                sell_again = input("Want to sell another product? [y/N]: ")
                    
                if sell_again == "N":
                    flag = False
                    
                
                self.shop = ProductManager("", 0, 0.0, 0.0, product_to_sell, quantity_sold)
                price = self.shop.sell_product()
                
                sells.append((quantity_sold, product_to_sell, price))

        except (ValueError,TypeError):
            print("Invalid value(s). Please try again.")
        
        
        if price is not None:
            
            if sells:
                print("SELL REGISTERED")
                total = 0.0
                for sell in sells:
                    quantity, product, price = sell
                    total += quantity * price
                    print(f"- {quantity} X {product}: ${price:.2f}")
                print(f"Total: ${total:.2f}")
                total = 0.0
            else:
                print("No sells were registered.")
            
        
    def calculate_profit(self):
        self.shop = ProductManager("", 0, 0.0, 0.0, "", 0)
        self.shop.calculate_profit()
            
if __name__ == "__main__":
    ui = UserInterface()
    ui.start()