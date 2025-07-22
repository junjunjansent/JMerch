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

  // Angular uses Observable instead of Promises
  // Observables allow emitting of multiple values over time, ideal for streams of data and UI changes
  // allow us to cancel request if client unsubscribes
  // compose operators to retry/debounce/timeout
  // Observables are also lazy, so HTTP request only execute when subscribed
  getProducts(): Observable<{ products: Product[] }> {
    return this.http.get<{ products: Product[] }>(this.productsURL);
  }

  getProductById(productId: number): Observable<{ product: Product }> {
    const productsURLwithId = `${this.productsURL}/${productId}`;
    return this.http.get<{ product: Product }>(productsURLwithId);
  }
}
