# Import necessary libraries
import codecademylib3  # Used for Codecademy runtime
import pandas as pd    # For data manipulation

# Load the datasets and parse the date columns
visits = pd.read_csv('visits.csv', parse_dates=[1])
cart = pd.read_csv('cart.csv', parse_dates=[1])
checkout = pd.read_csv('checkout.csv', parse_dates=[1])
purchase = pd.read_csv('purchase.csv', parse_dates=[1])

# Preview the first 10 rows of each DataFrame
print(visits.head(10))
print(cart.head(10))
print(checkout.head(10))
print(purchase.head(10))

# Step 1: Merge visits and cart DataFrames using a left join
visits_cart = pd.merge(visits, cart, how='left')

# Check the number of rows in the merged DataFrame
print(f"Number of rows in visits_cart: {len(visits_cart)}")

# Count how many users visited the site but did not add anything to the cart
null_cart = visits_cart['cart_time'].isnull().sum()
print(f"Users who visited but did not add to cart: {null_cart}")

# Step 2: Determine percentage of users who visited the site but did not proceed to checkout
visits_checkout = pd.merge(visits, checkout, how='left')
null_checkout = visits_checkout['checkout_time'].isnull().sum()

percent_no_checkout = round((null_checkout / len(visits_checkout)) * 100)
print(f"About {percent_no_checkout}% of visitors did not proceed to checkout.")

# Step 3: Determine percentage of users who added items to cart but did not checkout
cart_checkout = pd.merge(cart, checkout, how='left')
null_checkout_from_cart = cart_checkout['checkout_time'].isnull().sum()

percent_cart_no_checkout = round((null_checkout_from_cart / len(cart_checkout)) * 100)
print(f"About {percent_cart_no_checkout}% of users added items to cart but did not proceed to checkout.")

# Step 4: Merge all four steps of the funnel
# Merge visits → cart → checkout → purchase using left joins in order
all_data = visits.merge(cart, how='left')\
                 .merge(checkout, how='left')\
                 .merge(purchase, how='left')

# Display a preview of the complete funnel data
print(all_data.head())

# Step 5: Calculate percentage of users who reached checkout but did not complete purchase
null_purchase = all_data['purchase_time'].isnull().sum()
percent_checkout_no_purchase = round((null_purchase / len(all_data)) * 100)

print(f"About {percent_checkout_no_purchase}% of users who reached checkout did not complete the purchase.")

# Step 6: Calculate the average time from visit to purchase
# Create a new column for time difference
all_data['time_to_purchase'] = all_data['purchase_time'] - all_data['visit_time']

# Calculate the mean time to purchase
average_time_to_purchase = all_data['time_to_purchase'].mean()
print(f"Average time from visit to purchase: {average_time_to_purchase}")
