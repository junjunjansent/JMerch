import { Component, Input } from '@angular/core';
import { type Product } from '../../../core/types/product';
import { MatCardModule } from '@angular/material/card';
import { Router } from '@angular/router';
import { URLS } from '../../../core/routes/PATHS';

@Component({
  selector: 'product-card-vert',
  standalone: true,
  imports: [MatCardModule],
  templateUrl: './product-card-vert.component.html',
  // styleUrls: ['./product-card-vert.component.scss'],
})
export class ProductCardVertComponent {
  URLS = URLS;
  @Input() product!: Product;

  constructor(private router: Router) {}

  navigateToProduct() {
    const productId = this.product.id.toString();
    this.router.navigate([URLS.PUBLIC.BUY.PRODUCT_ONE(productId)]); // Replace with your URLS.PUBLIC.BUY.PRODUCT_ONE(productId)
  }
}
