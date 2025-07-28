import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { URLS } from '../../../routes/PATHS';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { Router } from 'express';
// import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-home',
  standalone: true,
  // imports: [RouterLink, MatCardModule, MatButtonModule],
  imports: [],
  templateUrl: './home2.component.html',
  styleUrls: ['./auth.scss'],
})
export default class HomeComponent {
  URLS = URLS;
}
