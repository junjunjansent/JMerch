import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'shop-product-one',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './product-one.component.html',
  //   styleUrl: './app.css', // TODO to modify
})
export class ProductOneComponent {}
