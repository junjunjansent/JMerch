export interface Cart {
  cart_owner_username: string;
  created_at: string;
  id: number;
  items: CartItem[];
  total_cost: string;
  updated_at: string;
}

export interface CartItem {
  category: string;
  default_delivery_time: number;
  design_name: string;
  display_photo: string;
  id: number;
  item_sub_total_cost: string;
  main_product_id: number;
  price: string;
  product_name: string;
  product_owner_username: string;
  product_variant_id: number;
  qty_available: number;
  qty_cart: number;
}
