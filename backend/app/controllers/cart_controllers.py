from app.db.db_connection import get_db_connection
from app.models.cart_model import show_cart_id, show_cart_item, destroy_cart_item, show_cart, create_cart, update_cart, destroy_cart
from app.models.products_model import show_product_variant_id
from app.utils.error_handler import raise_api_error, APIError
from app.utils.input_validator import number_range_validator
from datetime import datetime, timedelta

def show_cart_controller(user_id: str ) -> dict | None :
    try: 
        (connection, cursor) = get_db_connection()
        cart = show_cart(cursor, user_id)

        # check if cart does not exist, return null
        if not cart:
            return None
        
        # model - cart_model > show_cart would have filtered
        # deleted variant_ids, deleted or not active productId
        # if qty_cart <= 0
        # if qty_available <= 0 
        
        # model - delete cart if last updated is >15 days ago
        # model - check if cart Item is empty, delete cart
        is_cart_expired = cart.get("updated_at") and cart.get("updated_at") < datetime.utcnow() - timedelta(days=15)
        if not cart.get("items") or is_cart_expired:
            destroy_cart(cursor, user_id)
            connection.commit()
            return None

        return cart
    except Exception as err:
        connection.rollback()
        raise_api_error(err, pointer="cart_controllers.py")
    finally:
        cursor.close()
        connection.close()
    

def create_cart_controller(data: dict, user_id: str ) -> dict :
    qty_change = data.get("qtyChange")
    variant_id = str(data.get("variantId"))

    # validate qty
    qty_change = number_range_validator(qty_change, min=1)

    try:
        (connection, cursor) = get_db_connection()

         # model - check if variant exists
        variant = show_product_variant_id(cursor, user_id=user_id,variant_id=variant_id)
        if not variant:
            raise APIError(
                status=400,
                title="Bad Request: Variant",
                detail="Product Variant identified does not exist", 
                pointer="cart_controller.py > create_cart_controller")

        # model - check if cart exists
        existing_cart = show_cart_id(cursor, user_id)
        if existing_cart:
            raise APIError(
                status=403,
                title="Forbidden: Cart",
                detail="Cart already exists, cannot create another one", 
                pointer="cart_controller.py > create_cart_controller")

        new_cart = create_cart(cursor, user_id=user_id, variant_id=variant_id, qty_change=qty_change)
        connection.commit()

        new_cart = show_cart(cursor, user_id)
        return new_cart
    except Exception as err:
        connection.rollback()
        raise_api_error(err, pointer="cart_controller.py")
    finally:
        cursor.close()
        connection.close()

#  * updateCart can check if cart exists - create cart if necessary
#  * (1) checks if inputs from body are valid: itemId exists, qtyChange OR qtySet
#  * (2) looks to see if cart needs to be created
#  * (3) obtains info of item in cartItems
#  * (4) sets newQty via validated qtyChange or qtySet
#  * (5) updates item in cartItems
def update_cart_controller(data: dict, user_id: str ) -> dict :
    # extract values from data
    # // qtyChange: number that is not zero, //qtySet: up to productVarAvailableQty
    qty_change = data.get("qtyChange")  # from Add to Cart Buttons OR subtract in CartPage Buttons
    qty_set = data.get("qtySet")        # from Cart Page Buttons
    variant_id = data.get("variantId")

    # validate values
    qty_change = number_range_validator(qty_change) if qty_change else None
    qty_set = number_range_validator(qty_set, min=0) if qty_set else None
    # quick check only qtyChange or qtySet is given (written like this to handle zeros too)
    has_qty_change = qty_change is not None
    has_qty_set = qty_set is not None
    if (has_qty_change and has_qty_set) or (not has_qty_change and not has_qty_set):
        raise APIError(
            status=400,
            title="Bad Request: Different Qtys given",
            detail="Cart Item Qty can only be added/subtracted OR set, not both.",
            pointer="cart_controller.py > update_cart_controller")
    
    try:
        (connection, cursor) = get_db_connection()

        # model - check if variant exists
        variant = show_product_variant_id(cursor, user_id=user_id,variant_id=variant_id)
        if not variant:
            raise APIError(
                status=400,
                title="Bad Request: Variant",
                detail="Product Variant identified does not exist", 
                pointer="cart_controller.py > update_cart_controller")
        qty_available = variant["qty_available"]

        # model - check if cart exists, if no cart, create it
        existing_cart = show_cart_id(cursor, user_id)
        if not existing_cart:
            number_range_validator(qty_change, min=1)
            updated_cart = create_cart(cursor, user_id=user_id, variant_id=variant_id,qty_change=qty_change)
            connection.commit()
            return updated_cart

        # model - check cart_items to calculate new_qty
        cart_id = existing_cart["id"]
        cart_id = str(cart_id) if cart_id else None
        existing_cart_item = show_cart_item(cursor, cart_id=cart_id, variant_id=variant_id)
        qty_current = existing_cart_item["qty"] if existing_cart_item else 0
        # >> new_qty calculation
        if has_qty_change:
            qty_new = qty_current + qty_change 
        else:
            qty_new = qty_set
        qty_new = number_range_validator(qty_new,min=0, max=qty_available)
        
        # model - handle update
        cart_item_id = existing_cart_item["id"] if existing_cart_item else None
        cart_item_id = str(cart_item_id) if cart_item_id else None
        updated_cart = update_cart(cursor, cart_id=cart_id, cart_item_id=cart_item_id, variant_id=variant_id, qty_new=qty_new)        
        connection.commit()

        updated_cart = show_cart(cursor, user_id)
        return updated_cart
    except Exception as err:
        connection.rollback()
        raise_api_error(err, pointer="cart_controller.py")
    finally:
        cursor.close()
        connection.close()




def destroy_cart_controller(user_id: str ) -> dict :
    try: 
        (connection, cursor) = get_db_connection()

        # model - delete cart
        deleted_cart = destroy_cart(cursor, user_id)
        connection.commit()

        if not deleted_cart:
            raise APIError(
                status=404,
                title="Not Found: Cart",
                detail="Cart does not exist", 
                pointer="cart_controller.py > destroy_cart_controller")
        
        return deleted_cart  
    except Exception as err:
        connection.rollback()
        raise_api_error(err, pointer="cart_controllers.py")
    finally:
        cursor.close()
        connection.close()
