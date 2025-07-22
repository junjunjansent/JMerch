import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { Router } from '@angular/router';
import { URLS } from '../../../core/routes/PATHS';

import { CartService } from '../../../core/services/cart.service';
import { type Cart, type CartItem } from '../../../core/types/cart';
import { SnackBarService } from '../../../shared/service/snack-bar.service';

import dayjs from 'dayjs';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'buyer-cart',
  standalone: true,
  templateUrl: './cart.component.html',
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatTooltipModule,
  ],
  styleUrls: ['./cart.component.scss'],
})
export class CartComponent {
  cart: Cart | null = null;
  updated_at = '';
  isLoading = false;

  displayedColumns = [
    'photo',
    'product',
    'category',
    'quantity',
    'priceEach',
    'total',
    'actions',
  ];

  constructor(
    private cartService: CartService,
    private router: Router,
    private snackBar: SnackBarService
  ) {}

  ngOnInit(): void {
    this.loadCart();
  }

  loadCart(): void {
    this.isLoading = true;
    this.cartService.showCart().subscribe({
      next: (res) => {
        this.isLoading = false;
        this.updated_at = res.cart.updated_at
          ? dayjs(res.cart.updated_at).format('D MMM YYYY')
          : '';
        this.cart = res.cart;
      },
      error: (err) => {
        // console.log('Error: ', err.error.error);
        const errArray = err.error.error;
        this.snackBar.error(`${errArray[0].title} - ${errArray[0].detail}`);
        this.router.navigate([URLS.PUBLIC.SERVER]);
      },
    });
  }

  // clearCart(): void {
  //   // Confirm before clearing?
  //   if (!this.cart) return;
  //   this.isLoading = true;
  //   this.cartService.destroyCart().subscribe({
  //     next: () => {
  //       this.isLoading = false;
  //       this.cart = null;
  //     },
  //     error: (err) => {
  //       // console.log('Error: ', err.error.error);
  //       const errArray = err.error.error;
  //       this.snackBar.error(`${errArray[0].title} - ${errArray[0].detail}`);
  //       this.router.navigate([URLS.PUBLIC.SERVER]);
  //     },
  //   });
  // }

  // onQuantityChange(itemId: string, qtySet: number): void {
  //   this.isLoading = true;
  //   this.cartService
  //     .updateCart({ variantId: Number(itemId), qtySet }) // TODO: Fix type of ID haiz
  //     .subscribe({
  //       next: () => this.loadCart(),
  //       error: (err) => {
  //         // console.log('Error: ', err.error.error);
  //         const errArray = err.error.error;
  //         this.snackBar.error(`${errArray[0].title} - ${errArray[0].detail}`);
  //         this.router.navigate([URLS.PUBLIC.SERVER]);
  //       },
  //     });
  // }

  // navigateToShop(): void {
  //   this.router.navigate([URLS.PUBLIC.BUY.PRODUCT_ALL]);
  // }

  // navigateToCheckout(): void {
  //   if (!this.cart) return;
  //   this.router.navigate([URLS.USER().BUYER_CART.CHECKOUT]);
  // }
}
