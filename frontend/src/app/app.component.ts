import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import HomeComponent from './pages/index.page';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HomeComponent],
  template: `<app-home /><router-outlet />`,
})
export class AppComponent {}
