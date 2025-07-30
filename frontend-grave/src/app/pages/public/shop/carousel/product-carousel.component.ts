import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { type Product } from '../../../../core/types/product';
import { ProductCardCarouselComponent } from './product-card-carousel.component';

@Component({
  selector: 'product-carousel',
  standalone: true,
  imports: [CommonModule, ProductCardCarouselComponent],
  templateUrl: './product-carousel.component.html',
  // styleUrls: ['./product-carousel.component.scss'],
})
export class ProductCarouselComponent {
  @Input() products: Product[] = [];
}
