import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { URLS } from '../../../core/routes/PATHS';

import { AuthService } from '../../../core/auth.service';
import { ProductService } from '../../../core/services/product.service';
import { SnackBarService } from '../../../shared/service/snack-bar.service';
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
  styleUrls: ['./product-one.component.scss'],
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
    private productService: ProductService,
    private snackBar: SnackBarService
  ) {
    this.route.paramMap.subscribe((params) => {
      const id = Number(params.get('productId'));
      if (!id) {
        this.snackBar.error('Invalid product ID');
        this.router.navigate(['/']);
        return;
      }
      this.loadProduct(id);
    });
  }

  ngOnInit() {
    this.authService.isLoggedIn$.subscribe((loggedIn) => {
      this.isLoggedIn = loggedIn;
    });
  }

  loadProduct(id: number) {
    this.isLoading = true;
    this.productService.getProductById(id).subscribe({
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

    this.isAddingToCart = true;

    // Simulate async add to cart
    setTimeout(() => {
      this.isAddingToCart = false;
      this.snackBar.success('Added to cart!');
    }, 1000);
  }

  navigateToSignIn() {
    this.router.navigate([URLS.PUBLIC.SIGN_IN]);
  }
}
