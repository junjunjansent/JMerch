import psycopg2.extensions
from app.utils.error_handler import APIError

def convert_user_ids_to_usernames(cursor: psycopg2.extensions.cursor, user_ids: list[int]) -> list[str]:
    if not user_ids:
        return []
    # def find_username(user_id):
    #     cursor.execute("SELECT username FROM users WHERE id = %s;", (user_id,))
    #     return cursor.fetchone().get("username")
    # return [find_username(user_id) for user_id in user_ids]
    cursor.execute("SELECT username FROM users WHERE id = ANY(%s);", (user_ids,))
    username_dictionary = cursor.fetchall()
    return [entry[0] for entry in username_dictionary]

def show_product_variant_id(cursor: psycopg2.extensions.cursor, variant_id: str) -> dict:
    cursor.execute("""SELECT 
                        id, design_name, created_at, updated_at 
                   FROM product_variants 
                   WHERE id = %s""",
                     (variant_id,))
    return cursor.fetchone()

def index_products(cursor: psycopg2.extensions.cursor, user_id: str = None) -> list[dict]:
    # either viewable_to_users_list = NULL (viewable to ALL) or user_id in viewable_to_users_list
    # if product not active, maybe show diff colour
    # if product does not have variants, filter out --> INNER JOIN
    # >> from username: convert owner_user_id to their username
    # >> from variants: min price, max price, avail Qty, created_at (latest)
    # note if i use in aggregate function or have join, i need to indicate in GROUP BY
    sql_query = """
        SELECT 
            products.id,
            products.product_name,
            users.username AS owner_username,
            products.category,
            products.main_display_photo,
            products.is_active,
            MIN(variants.price) AS min_price,
            MAX(variants.price) AS max_price,
            SUM(variants.qty_available) AS qty_total_available,
            MAX(variants.created_at) AS newest_variant_created_at
        FROM products
            JOIN users ON products.owner_user_id = users.id
            JOIN product_variants AS variants ON variants.main_product_id = products.id
        WHERE (products.owner_user_id = %s) 
            OR (products.viewable_to_users_list IS NULL OR %s = ANY(products.viewable_to_users_list))
        GROUP BY products.id, users.username
        ORDER BY product_name ASC;"""
    cursor.execute(sql_query, (user_id, user_id))
    return cursor.fetchall()

def show_product(cursor: psycopg2.extensions.cursor, product_id: str, role: str = "buyer", user_id: str = None):
    # also to index all variants, {product: xx, variants: []}

    match role:
        case "buyer":
            sql_query_product= """
                SELECT 
                    products.id,
                    products.product_name,
                    products.product_description,
                    users.username AS owner_username,
                    products.category,
                    products.main_display_photo,
                    products.default_delivery_time,
                    products.created_at,
                    products.is_active
                FROM products
                    JOIN users ON products.owner_user_id = users.id
                WHERE products.id = %s
                    AND (products.owner_user_id = %s OR products.viewable_to_users_list IS NULL OR %s = ANY(products.viewable_to_users_list))"""
            sql_query_variants="""
                SELECT 
                    id AS variant_id,
                    design_name,
                    qty_available,
                    price,
                    display_photo,
                    created_at
                FROM product_variants AS variants
                WHERE main_product_id = %s
                ORDER BY created_at ASC;"""
            cursor.execute(sql_query_product, (product_id, user_id, user_id))
            product = cursor.fetchone()
            if product:
                cursor.execute(sql_query_variants, (product_id, ))
                product["variants"] = cursor.fetchall()

        case "seller":
            # products - can see viewable_to_users_list, updated_at (BUT need to convert)
            # variants - can see qty_inventory, updated_at
            sql_query_product= """
                SELECT 
                    products.id,
                    products.product_name,
                    products.product_description,
                    users.username AS owner_username,
                    products.category,
                    products.main_display_photo,
                    products.default_delivery_time,
                    products.created_at,
                    products.is_active,
                    products.viewable_to_users_list,
                    products.updated_at
                FROM products
                    JOIN users ON products.owner_user_id = users.id
                WHERE products.id = %s
                    AND (products.owner_user_id = %s OR products.viewable_to_users_list IS NULL OR %s = ANY(products.viewable_to_users_list))
            """
            sql_query_variants="""
                SELECT 
                    id,
                    design_name,
                    qty_available,
                    price,
                    display_photo,
                    created_at,
                    qty_inventory,
                    updated_at
                FROM product_variants AS variants
                WHERE main_product_id = %s
                ORDER BY created_at ASC;
            """
            cursor.execute(sql_query_product, (product_id, user_id, user_id))
            product = cursor.fetchone()
            if product:
                cursor.execute(sql_query_variants, (product_id,))
                product["variants"] = cursor.fetchall()

        case _:
            raise APIError(
                status=500,
                title="Internal Server Error: Products Database",
                detail="Invalid role given.", 
                pointer="products_model.py > show_product")

    # transform the list of IDs to usernames, not ordered
    if product and product.get("viewable_to_users_list"):
        product["viewable_to_users_list"] = convert_user_ids_to_usernames(product["viewable_to_users_list"])
    return product





# ----- AUTHORIZED -----

def create_product(cursor: psycopg2.extensions.cursor, ):
    try:
        return
    except Exception as err:
        err_name = err.__class__.__name__ or "Products Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="products_model.py > create_product")

def update_product(cursor: psycopg2.extensions.cursor, ):
    try:
        return
    except Exception as err:
        err_name = err.__class__.__name__ or "Products Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="products_model.py > update_product")

def create_product_variant(cursor: psycopg2.extensions.cursor, ):
    try:
        return
    except Exception as err:
        err_name = err.__class__.__name__ or "Products Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="products_model.py > create_product_variant")

def update_product_variant(cursor: psycopg2.extensions.cursor, ):
    try:
        return
    except Exception as err:
        err_name = err.__class__.__name__ or "Products Database"
        raise APIError(
            status=500,
            title=f"Internal Server Error: {err_name}",
            detail=str(err), 
            pointer="products_model.py > update_product_variant")
