import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { Router } from '@angular/router';
import { URLS } from '../../../core/routes/PATHS';

import dayjs from 'dayjs';
import { type Product } from '../../../core/types/product';
import { PublicService } from '../../../core/services/public.service';
import { ProductCardVertComponent } from '../../../shared/components/products/product-card-vert.component';

import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { SnackBarService } from '../../../shared/service/snack-bar.service';
import { ProductCarouselComponent } from './carousel/product-carousel.component';

@Component({
  selector: 'product-all',
  standalone: true,
  templateUrl: './product-all.component.html',
  // styleUrls: ['./product-all.component.scss'],
  imports: [
    CommonModule,
    ProductCardVertComponent,
    MatProgressSpinnerModule,
    ProductCarouselComponent,
  ],
})
export class ProductAllComponent {
  URLS = URLS;
  latestProducts: Product[] = [];
  allProducts: Product[] = [];
  isLoading = true;

  constructor(
    private publicService: PublicService,
    private router: Router,
    private snackBar: SnackBarService
  ) {
    this.loadAllProducts();
  }

  loadAllProducts() {
    this.publicService.getProducts().subscribe({
      next: (res) => {
        this.isLoading = false;
        this.allProducts = res.products;

        // set latestProducts using dayjs functions
        const sixMonthsAgo = dayjs().subtract(6, 'month');
        this.latestProducts = res.products.filter((product) =>
          dayjs(product.newest_variant_created_at).isAfter(sixMonthsAgo)
        );
      },
      error: (err) => {
        // console.log('Error: ', err.error.error);
        const errArray = err.error.error;
        this.snackBar.error(`${errArray[0].title} - ${errArray[0].detail}`);
        this.router.navigate([URLS.PUBLIC.SERVER]);
      },
    });
  }
}
