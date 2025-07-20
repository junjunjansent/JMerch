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
  //   styleUrls: ['./sign-up.component.css'],
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
  constructor(private fb: FormBuilder, private router: Router) {}

  formControlFromName(formControlName: string): FormControl {
    return this.signInForm.get(formControlName) as FormControl;
  }

  onSubmit() {
    const signInForm = this.signInForm;
    if (signInForm.valid) {
      console.log('Sign In Data:', signInForm.value);
      signInForm.reset();
      this.router.navigate([this.URLS.PUBLIC.HOME]);
    } else {
      signInForm.markAllAsTouched();
      console.log('fail');
    }
  }
}
