import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { URLS } from '../../../core/routes/PATHS';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink, MatCardModule, MatButtonModule, MatIconModule],
  templateUrl: './home.component.html',
  styleUrls: ['./register.scss'],
})
export class HomeComponent {
  URLS = URLS;
}
