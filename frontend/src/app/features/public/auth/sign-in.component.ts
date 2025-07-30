import { Component } from '@angular/core';
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
// import { AuthService } from '../../../core/auth.service';

@Component({
  selector: 'app-sign-in',
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
  templateUrl: './sign-in.component.html',
  styleUrls: ['./auth.css'],
})
export class SignInComponent {
  URLS = URLS;

  signInForm = this.fb.group({
    usernameOrEmail: new FormControl('', [
      Validators.required,
      Validators.minLength(4),
    ]),
    password: new FormControl('', [
      Validators.required,
      Validators.minLength(8),
    ]),
  });
  constructor(
    private fb: FormBuilder,
    // private authService: AuthService,
    private router: Router
  ) {}

  formControlFromName(formControlName: string): FormControl {
    return this.signInForm.get(formControlName) as FormControl;
  }

  onSubmit() {
    const signInForm = this.signInForm;
    const { usernameOrEmail, password } = signInForm.value;
    // if (signInForm.valid && usernameOrEmail && password) {
    //   this.authService.signIn({ usernameOrEmail, password }).subscribe({
    //     next: (res) => {
    //       // console.log('Signed In with token:', res.token);
    //       this.snackBar.success('Sign In Successful');
    //       signInForm.reset();
    //       this.router.navigate([this.URLS.PUBLIC.HOME]);
    //     },
    //     error: (err) => {
    //       const errArray = err.error.error;
    //       // console.log('Error: ', err.error.error);
    //       this.snackBar.error(`${errArray[0].title} - ${errArray[0].detail}`);
    //     },
    //   });
    // } else {
    //   signInForm.markAllAsTouched();
    // }
  }
}
