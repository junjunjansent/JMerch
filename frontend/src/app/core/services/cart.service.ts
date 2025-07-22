import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { type Cart, type CartItem } from '../types/cart';

@Injectable({
  providedIn: 'root',
})
export class CartService {
  private baseCartURL = `${import.meta.env['VITE_DEV_BASE_URL']}/cart`;

  constructor(private http: HttpClient) {}

  showCart(): Observable<{ cart: Cart }> {
    return this.http.get<{ cart: Cart }>(this.baseCartURL);
  }

  createCart(data: {
    qtyChange?: number;
    variantId: number;
  }): Observable<{ cart: Cart }> {
    return this.http.post<{ cart: Cart }>(this.baseCartURL, data);
  }

  updateCart(data: {
    qtyChange?: number;
    qtySet?: number;
    variantId: number;
  }): Observable<{ cart: Cart }> {
    return this.http.put<{ cart: Cart }>(this.baseCartURL, data);
  }

  destroyCart(): Observable<{ cart: { id: number; [key: string]: any } }> {
    return this.http.delete<{ cart: { id: number; [key: string]: any } }>(
      this.baseCartURL
    );
  }
}
