# import mysql.connector
# from mysql.connector import Error
#
#
# def get_db_connection():
#     """Helper function to get a new database connection."""
#     try:
#         cnx = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="root",
#             database="chatbot"
#         )
#         return cnx
#     except Error as e:
#         print(f"Error connecting to MySQL: {e}")
#         return None
#
#
# def get_order_status(order_id: int):
#     """Fetch the status of a given order_id from the database."""
#     try:
#         # Get a new connection
#         cnx = get_db_connection()
#         if cnx is None:
#             return "Database connection failed."
#
#         # Create a cursor object to interact with the database
#         cursor = cnx.cursor()
#
#         # Query to fetch the status of the given order_id
#         query = "SELECT status FROM order_track WHERE order_id = %s"
#
#         # Execute the query
#         cursor.execute(query, (order_id,))
#
#         # Fetch the result
#         result = cursor.fetchone()
#
#         # Close the cursor and connection
#         cursor.close()
#         cnx.close()
#
#         if result is not None:
#             return result[0]  # Return the status
#         else:
#             return None  # Handle case where no order is found
#
#     except Error as e:
#         print(f"Error occurred: {e}")
#         return "Error while fetching the order status."
#
#


import mysql.connector
global cnx
cnx = mysql.connector.connect(
        host="localhost",       # e.g., "localhost" if you're running MySQL locally
        user="root",   # e.g., "root"
        password="root",   # MySQL password
        database="chatbot"    # Name of the database containing the order_tracking table
    )

def get_total_order_price(order_id: int):

    try:
        cursor = cnx.cursor()
        # Call the stored function to get the total price
        query = "SELECT get_total_price(%s)"

        # Execute the query
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        # Check if there is a result and assign it to total_price
        if result[0] is not None:
            total_price = result[0]
            return total_price
        else:
            print(f"No price calculated for order ID {order_id}.")
            return None

    except Exception as e:
        print(f"Error during the total price calculation: {e}")

    # finally:
    #     cursor.close()

def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        #calling stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        cnx.commit()

        cursor.close()

        print("Order item inserted successfully")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")

        cnx.rollback()

        return -1

def get_next_orderid():
    cursor = cnx.cursor()

    # Query to fetch the status of the given order_id
    query = "SELECT max(order_id) from orders"

    # Execute the query
    cursor.execute(query)

    # Fetch the result (since order_id is unique, there should be only one result)
    result = cursor.fetchone()[0]
    # Close the cursor and connection
    cursor.close()

    if result is not None:
        return result + 1
    else:
        return 1

def get_order_status(order_id: int):
    # Create a cursor object to interact with the database
    cursor = cnx.cursor()

    # Query to fetch the status of the given order_id
    query = "SELECT status FROM order_track WHERE order_id = %s"

    # Execute the query
    cursor.execute(query, (order_id,))

    # Fetch the result (since order_id is unique, there should be only one result)
    result = cursor.fetchone()
    # Close the cursor and connection
    cursor.close()

    if result is not None:
        return result[0]
    else:
        return None

def insert_order_tracking(order_id , status):
    cursor = cnx.cursor()

    insert_query = "INSERT INTO order_track (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    cnx.commit()
    cursor.close()
