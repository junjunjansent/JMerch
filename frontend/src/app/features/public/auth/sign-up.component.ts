import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { URLS } from '../../../routes/PATHS';

import {
  FormBuilder,
  Validators,
  ReactiveFormsModule,
  FormControl,
} from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormFieldTextComponent } from '../../../shared/components/forms/form-field-text.component';
import { passwordsMatchValidator } from '../../../shared/utils/validator';
// import { AuthService } from '../../../core/auth.service';
import { SnackBarService } from '../../../shared/services/snack-bar.service';

@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    FormFieldTextComponent,
  ],
  templateUrl: './sign-up.component.html',
  styleUrls: ['./auth.scss'],
})
export class SignUpComponent {
  URLS = URLS;

  signUpForm = this.fb.group(
    {
      username: new FormControl('', [
        Validators.required,
        Validators.pattern(/^[a-z0-9_-]+$/),
        Validators.minLength(4),
      ]),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', [
        Validators.required,
        Validators.minLength(8),
      ]),
      confirmPassword: new FormControl('', [Validators.required]),
    },
    {
      validators: passwordsMatchValidator, // cross-field validator fn given
    }
  );
  constructor(
    private fb: FormBuilder,
    // private authService: AuthService,
    private router: Router,
    private snackBar: SnackBarService
  ) {}

  formControlFromName(formControlName: string): FormControl {
    return this.signUpForm.get(formControlName) as FormControl;
  }

  onSubmit() {
    const signUpForm = this.signUpForm;
    const { username, password, email } = signUpForm.value;

    // // angular forms and typescript validation dont seem compatible lol, do double check
    // if (signUpForm.valid && username && password && email) {
    //   this.authService.signUp({ username, password, email }).subscribe({
    //     next: (res) => {
    //       // console.log('Signed Up with token:', res.token);
    //       this.snackBar.success('Sign Up Successful');
    //       signUpForm.reset();
    //       this.router.navigate([this.URLS.PUBLIC.HOME]);
    //     },
    //     error: (err) => {
    //       // console.log('Error: ', err.error.error);
    //       const errArray = err.error.error;
    //       this.snackBar.error(`${errArray[0].title} - ${errArray[0].detail}`);
    //     },
    //   });
    // } else {
    //   signUpForm.markAllAsTouched();
    // }
  }
}
