export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
  gender?: string | null;
  phone_number?: string | null;
  birthday?: string | null;
  default_shipping_address?: string | null;
  profile_photo?: string | null;
  created_at: string;
  updated_at: string;
}
