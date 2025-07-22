import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { type Product } from '../types/product';

@Injectable({
  providedIn: 'root',
})
export class ProductService {
  private basePublicURL = `${import.meta.env['VITE_DEV_BASE_URL']}/public`;
  private productsURL = `${this.basePublicURL}/products`;

  constructor(private http: HttpClient) {}

  getProducts(): Observable<{ products: Product[] }> {
    return this.http.get<{ products: Product[] }>(this.productsURL);
  }

  getProductById(productId: number): Observable<{ product: Product }> {
    const productsURLwithId = `${this.productsURL}/${productId}`;
    return this.http.get<{ product: Product }>(productsURLwithId);
  }
}
