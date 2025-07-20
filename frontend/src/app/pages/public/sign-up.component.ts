import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { URLS } from '../../routes/PATHS';

import {
  FormBuilder,
  Validators,
  ReactiveFormsModule,
  FormControl,
} from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FormFieldTextComponent } from '../../shared/components/form-field-text.component';
import { passwordsMatchValidator } from '../../shared/validator';

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
  //   styleUrls: ['./sign-up.component.css'],
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
  constructor(private fb: FormBuilder, private router: Router) {}

  formControlFromName(formControlName: string): FormControl {
    return this.signUpForm.get(formControlName) as FormControl;
  }

  onSubmit() {
    const signUpForm = this.signUpForm;
    if (signUpForm.valid) {
      console.log('Sign Up Data:', signUpForm.value);
      signUpForm.reset();
      this.router.navigate([this.URLS.PUBLIC.HOME]);
    } else {
      signUpForm.markAllAsTouched();
      console.log('fail');
    }
  }
}
