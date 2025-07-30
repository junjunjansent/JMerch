import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { URLS } from '../../../core/routes/PATHS';

import { AuthService } from '../../../core/auth.service';
import { PublicService } from '../../../core/services/public.service';
import { SnackBarService } from '../../../shared/service/snack-bar.service';
import { CartService } from '../../../core/services/cart.service';
import { type Product, type Variant } from '../../../core/types/product';

import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatCardModule } from '@angular/material/card';
import { InfoTextCardComponent } from '../../../shared/components/info-text-card/info-text-card.component';

@Component({
  selector: 'product-one',
  standalone: true,
  imports: [
    CommonModule,
    MatProgressSpinnerModule,
    MatButtonModule,
    MatSelectModule,
    MatCardModule,
    InfoTextCardComponent,
  ],
  templateUrl: './product-one.component.html',
  // styleUrls: ['./product-one.component.scss'],
})
export class ProductOneComponent {
  product: Product | null = null;
  selectedVariantIndex = 0;
  qtyToAdd = 1;
  qtyOptions: number[] = [];
  isLoading = true;
  isAddingToCart = false;

  // observable states from AuthService
  isLoggedIn = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthService,
    private publicService: PublicService,
    private cartService: CartService,
    private snackBar: SnackBarService
  ) {
    this.route.paramMap.subscribe((params) => {
      const productId = Number(params.get('productId'));
      if (!productId) {
        this.snackBar.error('Invalid product ID');
        this.router.navigate(['/']);
        return;
      }
      this.loadProduct(productId);
    });
  }

  ngOnInit() {
    this.authService.isLoggedIn$.subscribe((loggedIn) => {
      this.isLoggedIn = loggedIn;
    });
  }

  loadProduct(id: number) {
    this.isLoading = true;
    this.publicService.getProductById(id).subscribe({
      next: (res) => {
        this.product = res.product;
        this.selectVariant(0);
        this.isLoading = false;
      },
      error: (err) => {
        const errArray = err.error.error;
        this.snackBar.error(`${errArray[0].title} - ${errArray[0].detail}`);
        this.router.navigate([URLS.PUBLIC.SERVER]);
      },
    });
  }

  get selectedVariant(): Variant | null {
    if (!this.product?.variants || this.selectedVariantIndex < 0) return null;
    return this.product.variants[this.selectedVariantIndex];
  }

  selectVariant(index: number) {
    this.selectedVariantIndex = index;
    const availableQty = this.selectedVariant?.qty_available ?? 1;
    this.qtyToAdd = 1;
    this.qtyOptions = Array.from({ length: availableQty }, (_, i) => i + 1);
  }

  handleAddToCart() {
    if (!this.isLoggedIn) {
      this.navigateToSignIn();
      return;
    }

    if (!this.selectedVariant) {
      this.snackBar.error('Select a Design First!');
      return;
    }
    this.isAddingToCart = true;
    const payload = {
      qtyChange: this.qtyToAdd,
      variantId: this.selectedVariant.variant_id,
    };

    this.cartService.updateCart(payload).subscribe({
      next: (res) => {
        this.isAddingToCart = false;
        this.snackBar.success(`Added ${this.qtyToAdd} to cart!`);
        this.qtyToAdd = 1;
      },
      error: (err) => {
        const errArray = err.error.error;
        this.snackBar.error(`${errArray[0].title} - ${errArray[0].detail}`);
        this.router.navigate([URLS.PUBLIC.SERVER]);
      },
    });
  }

  navigateToSignIn() {
    this.router.navigate([URLS.PUBLIC.SIGN_IN]);
  }
}
