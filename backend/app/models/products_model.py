import psycopg2.extensions
from app.utils.error_handler import APIError

def index_product(cursor: psycopg2.extensions.cursor, user_id: str) -> list[dict]:
    # either viewable_to_users_list = NULL (viewable to ALL) or user_id in viewable_to_users_list
    # if product not active, dont show
    # if product doesnt have variants, filter out --> INNER JOIN
    sql_query = """
        SELECT 
            products.id,
            products.product_name,
            users.username AS owner_username,
            products.category,
            products.main_display_photo,
            MIN(variants.price) AS min_price,
            MAX(variants.price) AS max_price,
            SUM(variants.qty_available) AS qty_total_available,
            MAX(variants.created_at) AS newest_variant_created_at
        FROM products
            JOIN users ON products.owner_user_id = users.id
            JOIN product_variants AS variants ON variants.main_product_id = products.id
        WHERE products.is_active = true 
            AND (products.viewable_to_users_list IS NULL OR %s = ANY(products.viewable_to_users_list))
        GROUP BY products.id, users.username
        ORDER BY latest_variant_created DESC;
    """
    
    cursor.execute(sql_query, (user_id,))
    return cursor.fetchall()
    
    
    
    
    
    # cursor.execute("SELECT id, product_name, owner_user_id, category, main_display_photo FROM products WHERE is_active = true AND viewable_to_users_list = NULL")
    

    # # to each product, i want to:
    # # translate owner_user_id to username from users
    # # search their product variant and inside the dictionary add these properties
    # # from variants: min price, max price, avail Qty, created_at (latest)
    # return cursor.fetchall()

def show_product(cursor: psycopg2.extensions.cursor, ):
    # also to index all variants
    return

# ----- AUTHORIZED -----

def create_product(cursor: psycopg2.extensions.cursor, ):
    try:
        return
    except Exception as err:
        raise APIError(
            status=500,
            title="Internal Server Error: Products Database",
            detail=str(err), 
            pointer="products_model.py > create_product")

def update_product(cursor: psycopg2.extensions.cursor, ):
    try:
        return
    except Exception as err:
        raise APIError(
            status=500,
            title="Internal Server Error: Products Database",
            detail=str(err), 
            pointer="products_model.py > update_product")

def create_product_variant(cursor: psycopg2.extensions.cursor, ):
    try:
        return
    except Exception as err:
        raise APIError(
            status=500,
            title="Internal Server Error: Product Variants Database",
            detail=str(err), 
            pointer="products_model.py > create_product_variant")

def update_product_variant(cursor: psycopg2.extensions.cursor, ):
    try:
        return
    except Exception as err:
        raise APIError(
            status=500,
            title="Internal Server Error: Product Variants Database",
            detail=str(err), 
            pointer="products_model.py > update_product_variant")
