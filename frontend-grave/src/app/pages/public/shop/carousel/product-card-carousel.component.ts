import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

import { type Product } from '../../../../core/types/product';
import { MatCardModule } from '@angular/material/card';

import { Router } from '@angular/router';
import { URLS } from '../../../../core/routes/PATHS';

@Component({
  selector: 'product-card-carousel',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  templateUrl: './product-card-carousel.component.html',
  // styleUrls: ['./product-card-carousel.component.scss'],
})
export class ProductCardCarouselComponent {
  @Input() product!: Product;
  URLS = URLS;

  constructor(private router: Router) {}

  navigateToProduct() {
    const productId = this.product.id.toString();
    this.router.navigate([URLS.PUBLIC.BUY.PRODUCT_ONE(productId)]); // Replace with your URLS.PUBLIC.BUY.PRODUCT_ONE(productId)
  }
}
