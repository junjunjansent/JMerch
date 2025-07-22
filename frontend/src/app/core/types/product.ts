export interface Product {
  id: number;
  category: string;
  is_active: boolean;
  main_display_photo: string;
  max_price: string;
  min_price: string;
  newest_variant_created_at: string;
  owner_username: string;
  product_name: string;
  qty_total_available: number;
  product_description?: string | null;
  default_delivery_time?: number;
  created_at?: string;
  variants?: Variant[];
}
export interface Variant {
  variant_id: number;
  design_name: string;
  display_photo: string;
  price: number;
  qty_available: number;
  created_at: string;
}
