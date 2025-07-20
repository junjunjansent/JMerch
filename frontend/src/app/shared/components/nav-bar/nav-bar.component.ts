import { Component } from '@angular/core';

import { URLS } from '../../../routes/PATHS';
import { RouterModule } from '@angular/router';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatMenuModule } from '@angular/material/menu';
import { MatButtonModule } from '@angular/material/button';
import { NavItemBtnComponent } from './nav-item-btn.component';

@Component({
  selector: 'app-nav-bar',
  standalone: true,
  imports: [
    RouterModule,
    MatToolbarModule,
    MatMenuModule,
    MatButtonModule,
    NavItemBtnComponent,
  ], // for routeLink & routeActive
  templateUrl: './nav-bar.component.html',
})
export class NavBarComponent {
  URLS = URLS;

  userUsername = String(1); // i need userUsername
}
