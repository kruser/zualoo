stores = [
    "A&P",
    "Acme Markets",
    "Albertsons",
    "ALDI",
    "AP Fresh",
    "ASDA",
    "Bi-Lo",
    "Bohning's Supermarket",
    "Brookshire Grocery Company",
    "Central Market",
    "Coles",
    "Copps",
    "Costco",
    "Cumberland Farms",
    "Cub Foods",
    "County Market",
    "Delhaize",
    "Farm Boy",
    "Food Emporium",
    "FoodLand",
    "Food Lion",
    "Fred Meyer",
    "Giant Eagle",
    "Grocery Store",
    "Haggen",
    "H-E-B",
    "Harris Teeter",
    "Herbie's",
    "Hy-Vee",
    "IGA",
    "Jewel",
    "Jungle Jim's International Market",
    "Key Food",
    "Kroger",
    "Loblaws",
    "Loeb",
    "Lowes Foods",
    "Marketplace Foods",
    "Maxi",
    "Meijer",
    "Metro",
    "Morrisons",
    "Pathmark",
    "Piggly Wiggly",
    "Price Chopper",
    "Provigo",
    "Publix",
    "PW's",
    "QFC",
    "Rainbow Foods",
    "Ralphs",
    "Randalls",
    "Reasor's Grocery",
    "Safeway",
    "Sainsbury's",
    "Sam's Club",
    "Save-a-Lot",
    "Save-On-Foods",
    "Schnucks",
    "Shaws",
    "Shoprite",
    "Smith's Food and Drug",
    "Sobeys",
    "Somerfield",
    "Spartan",
    "Stater Bros.",
    "Stewart's Shops",
    "Stop & Shop",
    "Super C",
    "Supervalu",
    "Target",
    "The Big Apple",
    "The Fresh Market",
    "Tops",
    "Trader Joe's",
    "Vons",
    "Waldbaum's",
    "Walmart",
    "Wegmans",
    "Whole Foods Market",
    "Winn-Dixie",
]

sections = {'Bakery & Breads': [('Bagels', False),
                       ('Specialty Bread', False),
                       ('Seeded Rye Bread', True),
                       ('Whole Wheat Bread', True),
                       ('Cakes', False),
                       ('Cookies', False),
                       ('Croissants', False),
                       ('Donuts', False),
                       ('French Bread', False),
                       ('Muffins', False),
                       ('Pastries', False),
                       ('Tortillas', False),
                       ('Pitas', False),
                       ('Rolls', False)],
 'Dairy': [('Biscuits', False),
           ('Butter', True),
           ('Margarine', False),
           ('Coffee Creamer', True),
           ('Cookies', False),
           ('Cottage Cheese', False),
           ('Cream Cheese', True),
           ('Eggs', True),
           ('Orange Juice', True),
           ('Milk', True),
           ('Parmesan', False),
           ('Refrigerated Dough', False),
           ('Sour Cream', True),
           ('Yogurt', False),
           ('Drinkable Yogurts', True)],
 'Deli': [('Olives', True),
          ('Sandwiches', False),
          ('Fried Chicken', False),
          ('Rotisserie Chicken', True),
          ('Party Trays', False),
          ('Prepared Salads', False),
          ('Delicatessen Crackers', False),
          ('Brie', False),
          ('Cheddar', False),
          ('Feta', False),
          ('Gouda', False),
          ('Havarti', False),
          ('Muenster', False),
          ('Monterey Jack', False),
          ('Mozzarella', False),
          ('Parmesan', False),
          ('Provolone', False),
          ('Ricotta', False),
          ('Swiss', False),
          ('Gruyere', False),
          ('Emmenthaler', False),
          ('Salami', True),
          ('Ham', True)],
 'Floral': [('Arrangements', False),
            ('Balloons', False),
            ('Bouquets', False),
            ('Cut Flowers', False),
            ('Dried Flowers', False),
            ('Vases', False)],
 'Frozen Breakfasts': [('Waffles', False),
                       ('Toaster Strudel', False),
                       ('Pancakes', False),],
 'Frozen Dinners': [('Frozen Meat', False),
                  ('Frozen Seafood', False),
                  ('Frozen Lasagna', False),
                  ('Frozen Pizza', False),
                  ('Chicken Nuggets', True)],
 'Frozen Vegetables & Fruits': [('Frozen Strawberries', False),
                       ('Frozen Blueberries', False),
                       ('Frozen Corn', False),
                       ('Frozen Peas', False)],
 'Frozen Desserts': [('Ice Cream', False),
                       ('Ice Cream Sandwiches', False),
                       ('Whipped Cream', False)],
 'Baking Goods & Supplies': [('Flour', False),
                  ('Sugar', False),
                  ('Powdered Sugar', False),
                  ('Baking Powder', False),
                  ('Vegetable Oil', False),
                  ('Canola Oil', False),
                  ('Baking Soda', True)],
 'Snacks': [('Potato Chips', False),
                  ('Tortilla Chips', False),
                  ('Popcorn', False),
                  ('Pringles', False),
                  ('Cheetos', False),
                  ('Cheese Puffs', False),
                  ('Peanuts', True)],
 'Condiments': [('Ketchup', False),
                  ('Salad Dressing', False),
                  ('Mayonnaise', False),
                  ('Mustard', False),
                  ('Peanut Butter', False),
                  ('Pickles', False),
                  ('Jelly', False),
                  ('Jam', True)],
 'Canned Goods & Soup': [('Canned Tomatoes', False),
                  ('Canned Corn', False),
                  ('Canned Soup', False),
                  ('Canned Fruit', False),
                  ('Refried Beans', False),
                  ('Black Beans', False),
                  ('Garbanzo Beans', True)],
 'Pasta': [('Spaghetti', False),
                  ('Spaghetti Sauce', False),
                  ('Lasagna Noodles', False)],
 'Paper Goods & Cleaning': [('Garbage Bags', False),
                  ('Sandwich Bags', False),
                  ('Paper Plates', False),
                  ('Paper Cups', False),
                  ('Plastic Cups', False),
                  ('Plastic Forks', False),
                  ('Plastic Spoons', False),
                  ('Dish soap', False),
                  ('Aluminum Foil', True),
                  ('Ziploc Bags', True),
                  ('Paper Towels', True),
                  ('Toilet Paper', True),
                  ('Napkins', True),
                  ('Laundry Detergent', False),
                  ('Dishwashing Detergent', False),
                  ('Windex', True)],
 'Cereal': [('Frosted Mini Wheats', False),
                  ('Cocoa Puffs', False),
                  ('Cherrios', False),
                  ('Corn Flakes', False),
                  ('Raisin Bran', False),
                  ('Syrup', False),
                  ('Instant Oatmeal', False),
                  ('Oatmeal', False),
                  ('Cracklin Oat Bran', False),
                  ('Honey Nut Cherrios', False),
                  ('Fruit Loops', False),
                  ('Cap\'n Crunch', False),
                  ('Peanut Butter Crunch', False),
                  ('Wheaties', False),
                  ('Pancake Mix', False),
                  ('Syrup', False),
                  ('Maple Syrup', True)],
 'Drinks': [('Coffee', False),
                  ('Tea', False),
                  ('Mountain Dew', False),
                  ('Soda', False),
                  ('Coke', False),
                  ('Diet Coke', False),
                  ('Pepsi', False),
                  ('Diet Pepsi', False),
                  ('Root Beer', True)],
 'Alcohol': [('Wine', False),
                  ('Beer', False)],
 'Lunch Meat and Cheese': [('Packaged Meat', False),
                           ('Packaged Cheese', False),
                           ('Bologna', False),
                           ('Lunch Kits', False),
                           ('Shredded Cheese', True),
                           ('Cheese Slices', True),
                           ('Ham', True)],
 'Meat': [('Bacon', True),
          ('Chicken Breasts', True),
          ('Ground Beef', True),
          ('Ham', False),
          ('Hot Dogs', True),
          ('Liver', False),
          ('Pork', False),
          ('Ribs', False),
          ('Roast', False),
          ('Sausage', False),
          ('Steaks', True),
          ('Turkey', False)],
 'Pharmacy / Drugstore': [('Cosmetics', False),
                          ('Prescriptions', False),
                          ('Medical Aids', False),
                          ('OTC Medicines', False),
                          ('Shaving Supplies', False),
                          ('Razor Blades', True),
                          ('Shaving Cream', True),
                          ('Toothpaste', True),
                          ('Mouthwash', False),
                          ('Supplements', False),
                          ('Shampoo', False),
                          ('Body Wash', False),
                          ('Deoderant', False),
                          ('Vitamins', False)],
 'Photo': [('Photo processing', False),
           ('Film', False),
           ('Batteries', False),
           ('Camera', False),
           ('Albums', False),
           ('Frames', False)],
 'Produce': [('Apples', True),
             ('Avocados', False),
             ('Bananas', True),
             ('Beans', False),
             ('Beets', False),
             ('Broccoli', True),
             ('Cabbage', False),
             ('Carrots', True),
             ('Cauliflower', False),
             ('Celery', True),
             ('Cherries', False),
             ('Corn', False),
             ('Cucumbers', False),
             ('Salsa', False),
             ('Garlic', True),
             ('Grapefruit', False),
             ('Grapes', True),
             ('Lemons', False),
             ('Lettuce', True),
             ('Limes', False),
             ('Melons', False),
             ('Mushrooms', False),
             ('Onions', True),
             ('Oranges', False),
             ('Party Tray', False),
             ('Pears', True),
             ('Peas', False),
             ('Peppers', False),
             ('Potatoes', True),
             ('Strawberries', True),
             ('Spinach', True),
             ('Squash', False),
             ('Tomatoes', False),
             ('Watermelon', False)],
 'Seafood': [('Shrimp', False),
             ('Crab', False),
             ('Catfish', False),
             ('Salmon', False),
             ('Tilapia', False),
             ('Fish Fry', False),
             ('Cocktail Sauce', False),
             ('Tartar Sauce', False),
             ('Seafood Salad', False),
             ('Shrimp Platter', False)]}