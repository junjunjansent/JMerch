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

# const updateCart = async (req, res, next) => {
#   try {
#     // qtyChange: number that is not zero, //qtySet: up to productVarAvailableQty
#     const { itemId, qtyChange, qtySet } = req.body;

#     // quick check only qtyChange or qtySet is given (written like this to handle zeros too)
#     const hasQtyChange = qtyChange !== undefined;
#     const hasQtySet = qtySet !== undefined;
#     if ((hasQtyChange && hasQtySet) || (!hasQtyChange && !hasQtySet)) {
#       throw new ApiError({
#         status: 400,
#         source: { pointer: "cartController.js" },
#         title: "Bad Request: Too many requests to Qty",
#         detail: "Cart Item Qty can only be added/subtracted OR set, not both.",
#       });
#     }

#     // check if item exists in Shop
#     // if item doesnt exists in Product Var, delete
#     // if item's mainProduct doesnt exist Product, delete
#     // if !item.mainProduct.isActive, delete
#     const itemExisting = await ProductVariant.findById(itemId)
#       .select("mainProduct productVarAvailableQty")
#       .populate({
#         path: "mainProduct",
#         select: "productIsActive",
#       });
#     const isExistingItem =
#       itemExisting &&
#       itemExisting.mainProduct &&
#       itemExisting.mainProduct.productIsActive;
#     if (!isExistingItem) {
#       throw new ApiError({
#         status: 410,
#         source: { pointer: "cartController.js" },
#         title: "Gone: Product Var Item does not Exist",
#         detail: "Selected Product Var Item no longer exists.",
#       });
#     }

#     // -------- get all cart details (selected fields) - but mongoose can only do nested populate if defined
#     const user = getUserFromRequest(req);
#     const cart = await Cart.findOne({ buyer: user._id }).select("cartItems");

#     // const { cartId } = req.params;
#     // if (!cartId) {
#     //   throw new ApiError({
#     //     status: 400,
#     //     source: { pointer: "cartController.js" },
#     //     title: "Bad Request: No Cart ID Given",
#     //     detail: "No Cart ID was passed for update.",
#     //   });
#     // }

#     if (!cart) {
#       // create cart if it doesnt exist
#       const qtyChangeValidated = numberRangeValidator(qtyChange, { min: 1 });
#       const newCart = await Cart.create({
#         buyer: user._id,
#         cartItems: [{ item: itemId, qty: qtyChangeValidated }],
#       });
#       return res.status(201).json({ cart: newCart });
#     }

#     // check if item exists in Cart - gets index in cartItems and qty
#     // if no item in cart, will need to add new Item
#     const itemIndexinCartItems = cart.cartItems.findIndex(({ item }) =>
#       item._id.equals(itemId)
#     );
#     const currentQty =
#       itemIndexinCartItems === -1
#         ? 0
#         : cart.cartItems[itemIndexinCartItems].qty;
#     let newQty = currentQty;

#     // -------- checking for qtyChange & qty Set
#     if (hasQtyChange) {
#       const qtyChangeValidated = numberRangeValidator(qtyChange, {
#         min: -Infinity,
#       });
#       if (qtyChangeValidated === 0) {
#         throw new ApiError({
#           status: 400,
#           source: { pointer: "cartController.js" },
#           title: "Bad Request: QtyChange given is 0",
#           detail: "No change requested to Cart Item Qty.",
#         });
#       }
#       newQty = currentQty + qtyChangeValidated;
#     } else if (hasQtySet) {
#       const qtySetValidated = numberRangeValidator(qtySet);
#       newQty = qtySetValidated;
#     }

#     // ——------ handle newQty

#     if (newQty < 0) {
#       throw new ApiError({
#         status: 400,
#         source: { pointer: "cartController.js" },
#         title: "Bad Request: newQty becomes a negative number",
#         detail: "Cannot make Cart Item Qty to a negative number.",
#       });
#     } else if (newQty === 0) {
#       cart.cartItems.pull({ item: itemId });
#     } else if (newQty <= itemExisting.productVarAvailableQty) {
#       if (itemIndexinCartItems === -1) {
#         cart.cartItems.push({ item: itemId, qty: newQty });
#       } else {
#         cart.cartItems[itemIndexinCartItems].qty = newQty;
#       }
#     } else if (newQty > itemExisting.productVarAvailableQty) {
#       throw new ApiError({
#         status: 400,
#         source: { pointer: "cartController.js" },
#         title: "Bad Request: newQty too large",
#         detail: `newQty cannot be larger than selected item's available Qty - ${itemExisting.productVarAvailableQty}.`,
#       });
#     }

#     await cart.save();

#     res.status(201).json({ cart });

#     // // TODO: need some logic to start saving Qtys as not available if it's in someone's cart (maybe in checkout?)
#   } catch (err) {
#     next(err);
#   }
# };




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
