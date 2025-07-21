import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { map } from 'rxjs';

import { URLS } from '../../../routes/PATHS';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatMenuModule } from '@angular/material/menu';
import { MatButtonModule } from '@angular/material/button';
import { NavItemBtnComponent } from './nav-item-btn.component';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/auth.service';
import { SnackBarService } from '../../service/snack-bar.service';

@Component({
  selector: 'app-nav-bar',
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatMenuModule,
    MatButtonModule,
    NavItemBtnComponent,
  ],
  templateUrl: './nav-bar.component.html',
})
export class NavBarComponent {
  URLS = URLS;

  // observable states from AuthService
  isLoggedIn = false;
  userUsername: string = '';

  // userUsername = String(1); // i need userUsername

  constructor(
    private router: Router,
    private authService: AuthService,
    private snackBar: SnackBarService
  ) {}

  ngOnInit() {
    this.authService.isLoggedIn$.subscribe((loggedIn) => {
      this.isLoggedIn = loggedIn;
      this.userUsername = loggedIn
        ? this.authService.getUsernameFromToken()
        : '';
    });
  }

  signOut() {
    this.authService.signOut();
    this.snackBar.success('Sign Out Successful');
    this.router.navigate([this.URLS.PUBLIC.HOME]);
  }
}
