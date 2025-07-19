import { Component } from '@angular/core';

import { URLS } from '../../../routes/PATHS';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-nav-bar',
  standalone: true,
  imports: [RouterModule], // for routeLink & routeActive
  templateUrl: './nav-bar.component.html',
  //   styleUrls: ['./nav-bar.component.css'],
})
export class NavBarComponent {
  URLS = URLS;

  userUsername = String(1); // i need userUsername
}
