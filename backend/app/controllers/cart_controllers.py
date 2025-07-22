from app.db.db_connection import get_db_connection
from app.models.cart_model import show_cart_id, show_cart, create_cart, update_cart, destroy_cart
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
        if cart.get("items") or is_cart_expired:
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
        return new_cart
    except Exception as err:
        connection.rollback()
        raise_api_error(err, pointer="cart_controller.py")
    finally:
        cursor.close()
        connection.close()


def update_cart_controller(data: dict, user_id: str ) -> dict :
    return



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
