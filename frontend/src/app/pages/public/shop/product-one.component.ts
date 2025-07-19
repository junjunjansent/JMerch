import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'shop-product-all',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './product-all.component.html',
  //   styleUrl: './app.css', // TODO to modify
})
export class ProductAllComponent {}
