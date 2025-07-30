import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import { Router } from '@angular/router';
import { URLS } from '../../../core/routes/PATHS';

import { UserService } from '../../../core/services/user.service';
import { UserProfile } from '../../../core/types/user';
import { SnackBarService } from '../../../shared/service/snack-bar.service';

import dayjs from 'dayjs';

import { MatProgressSpinner } from '@angular/material/progress-spinner';
import { MatIcon } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatButton } from '@angular/material/button';
import { InfoTextCardComponent } from '../../../shared/components/info-text-card/info-text-card.component';

@Component({
  selector: 'abt-main',
  standalone: true,
  imports: [
    CommonModule,
    MatProgressSpinner,
    MatListModule,
    MatIcon,
    MatButton,
    InfoTextCardComponent,
  ],
  templateUrl: './about-main.component.html',
  // styleUrls: ['./about.component.scss'],
})
export class AboutMainComponent {
  userProfile!: UserProfile;
  username = '';
  created_at = '';
  userInfoGroups: Array<Array<{ label: string; value: string }>> = [];
  isLoading = true;
  hasError = false;

  constructor(
    private userService: UserService,
    private router: Router,
    private snackBar: SnackBarService
  ) {
    this.loadUserProfile();
  }

  loadUserProfile() {
    this.userService.showOwnerProfile().subscribe({
      next: (res) => {
        this.userProfile = res.user;
        this.username = res.user.username;
        this.created_at = dayjs(res.user.created_at).format('D MMM YYYY');
        this.userInfoGroups = [
          [
            { label: 'Username', value: res.user.username },
            { label: 'Email', value: res.user.email },
          ],
          [
            { label: 'First Name', value: res.user.first_name ?? '-' },
            { label: 'Last Name', value: res.user.last_name ?? '-' },
            { label: 'Gender', value: res.user.gender ?? '-' },
          ],
          [
            { label: 'Phone Number', value: res.user.phone_number ?? '-' },
            {
              label: 'Birthday',
              value: res.user.birthday
                ? dayjs(res.user.birthday).format('D MMM YYYY')
                : '-',
            },
          ],
          [
            {
              label: 'Default Shipping Address',
              value: res.user.default_shipping_address ?? '-',
            },
          ],
        ];
        this.isLoading = false;
      },
      error: (err) => {
        // console.log('Error: ', err.error.error);
        console.error('Error fetching user profile:', err);
        const errArray = err.error.error;
        this.snackBar.error(`${errArray[0].title} - ${errArray[0].detail}`);
        this.router.navigate([URLS.PUBLIC.SERVER]); // or your URLS.PUBLIC.ERROR path
      },
    });
  }

  navigateToEditProfile() {
    this.router.navigate([URLS.USER(this.username).ABOUT.EDIT_PROFILE], {
      state: { userProfile: this.userProfile },
    });
  }

  navigateToEditPassword() {
    this.router.navigate([URLS.USER(this.username).ABOUT.EDIT_PASSWORD]);
  }
}
