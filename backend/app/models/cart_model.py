import psycopg2.extensions
from app.utils.error_handler import APIError

def show_cart_id(cursor: psycopg2.extensions.cursor, user_id: str) -> dict:
    cursor.execute("""SELECT 
                        id, created_at, updated_at 
                   FROM carts 
                   WHERE buyer_user_id = %s""",
                     (user_id,))
    return cursor.fetchone()

def show_cart(cursor: psycopg2.extensions.cursor, user_id: str ) -> dict :
    # do calculation and filtering here. dont show:
    # if product not active
    # if qty_avail < 0
    # if qty_cart < 0
    sql_query_cart="""
        SELECT
            carts.id,
            users.username AS cart_owner_username,
            carts.created_at,
            carts.updated_at
        FROM carts
            JOIN users ON carts.buyer_user_id = users.id
        WHERE carts.buyer_user_id = %s"""
    sql_query_items="""
        SELECT
            items.id,
            items.product_variant_id,
            items.qty AS qty_cart,
            variants.main_product_id, 
            variants.design_name,
            variants.qty_available,
            variants.price,
            (items.qty * variants.price) AS item_sub_total_cost,
            variants.display_photo,
            products.product_name,
            products.category,
            products.default_delivery_time,
            users.username AS product_owner_username
        FROM cart_items AS items
            JOIN product_variants AS variants ON items.product_variant_id = variants.id
            JOIN products ON variants.main_product_id = products.id
            JOIN users ON products.owner_user_id = users.id
        WHERE cart_id = %s
            AND items.qty > 0
            AND products.is_active = true
            AND variants.qty_available > 0
            AND (products.owner_user_id = %s OR products.viewable_to_users_list IS NULL OR %s = ANY(products.viewable_to_users_list))"""

    cursor.execute(sql_query_cart, (user_id, ))
    cart = cursor.fetchone()
    if cart:
        cart_id = cart["id"]
        cursor.execute(sql_query_items, (cart_id, user_id, user_id))
        items = cursor.fetchall()
        cart["items"] = items
        # calculate total also
        cart["total_cost"] = round(sum(item["item_sub_total_cost"] for item in items), 2)

    return cart

def create_cart(cursor: psycopg2.extensions.cursor, *, user_id: str, variant_id: str, qty_change: int ) -> dict :
    try:
        # create cart
        cursor.execute("""INSERT INTO carts 
                            (buyer_user_id) 
                       VALUES (%s)""", 
                       (user_id,))
        cart_id = show_cart_id(cursor, user_id)["id"]

        # create cart_items
        create_cart_item(cursor, cart_id=cart_id, variant_id=variant_id, qty_change=qty_change)

        # give back mini cart object (id, created_at, updated_at)
        return show_cart_id(cursor, user_id)

    except Exception as err:
        err_name = err.__class__.__name__ or "Cart Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="cart_model.py > create_cart")

#  * updateCart can check if cart exists - create cart if necessary
#  * (1) checks if inputs from body are valid: itemId exists, qtyChange OR qtySet
#  * (2) looks to see if cart needs to be created
#  * (3) obtains info of item in cartItems
#  * (4) sets newQty via validated qtyChange or qtySet
#  * (5) updates item in cartItems
def update_cart(cursor: psycopg2.extensions.cursor, *, cart_id: str, cart_item_id: str = None, variant_id: str, qty_new: int ) -> dict :
    try:
        if qty_new == 0 and cart_item_id:
            destroy_cart_item(cursor, cart_id=cart_id, variant_id=variant_id)
        elif not cart_item_id:
            create_cart_item(cursor, cart_id=cart_id, variant_id=variant_id,qty_change=qty_new)
        else: 
            update_cart_item(cursor, cart_id=cart_id, variant_id=variant_id, qty_new=qty_new)

        cursor.execute("UPDATE carts SET updated_at = CURRENT_TIMESTAMP WHERE id = %s;",(cart_id,))
        cursor.execute("""SELECT 
                        id, created_at, updated_at 
                   FROM carts 
                   WHERE id = %s""",
                     (cart_id,))
        return cursor.fetchone()
    except Exception as err:
        err_name = err.__class__.__name__ or "Cart Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="cart_model.py > update_cart")


def destroy_cart(cursor: psycopg2.extensions.cursor, user_id: str ) -> dict :
    try:   
        #find cart first
        cart = show_cart_id(cursor, user_id)

        #delete cart
        cursor.execute("DELETE FROM carts WHERE buyer_user_id = %s;",
                        (user_id,))

        return cart
    except Exception as err:
        err_name = err.__class__.__name__ or "Cart Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="cart_model.py > destroy_cart")


# ---------- Cart Item

def show_cart_item(cursor: psycopg2.extensions.cursor, *, cart_id: str, variant_id: str) -> dict:
    cursor.execute("""SELECT 
                        id, qty 
                   FROM cart_items 
                   WHERE cart_id = %s AND product_variant_id = %s""",
                     (cart_id, variant_id))
    return cursor.fetchone()


def create_cart_item(cursor: psycopg2.extensions.cursor, *, cart_id: str, variant_id: str, qty_change: int) -> dict:
    try:
        cursor.execute("""INSERT INTO cart_items 
                            (cart_id, product_variant_id, qty)
                        VALUES (%s, %s, %s)""",
                        (cart_id, variant_id, qty_change))

        return show_cart_item(cursor, cart_id=cart_id, variant_id=variant_id)
    except Exception as err:
        err_name = err.__class__.__name__ or "Cart Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="cart_model.py > create_cart_item")

def update_cart_item(cursor: psycopg2.extensions.cursor, *, cart_id: str, variant_id: str, qty_new: int) -> dict:
    try:
        cursor.execute("""UPDATE cart_items 
                        SET qty = %s
                        WHERE cart_id = %s AND product_variant_id = %s""",
                        (qty_new, cart_id, variant_id))

        return show_cart_item(cursor, cart_id=cart_id, variant_id=variant_id)
    except Exception as err:
        err_name = err.__class__.__name__ or "Cart Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="cart_model.py > update_cart_item")

def destroy_cart_item(cursor: psycopg2.extensions.cursor, *, cart_id: str, variant_id: str) -> dict:
    try:
        # find item
        cart_item = show_cart_item(cursor, cart_id=cart_id, variant_id=variant_id)
        
        cursor.execute("""DELETE FROM cart_items 
                        WHERE cart_id=%s AND product_variant_id = %s;""",
                        (cart_id, variant_id))
        return cart_item
    except Exception as err:
        err_name = err.__class__.__name__ or "Cart Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="cart_model.py > destroy_cart_item")
