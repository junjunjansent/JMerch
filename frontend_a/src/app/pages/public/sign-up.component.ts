import { Component } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-sign-up',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './sign-up.component.html',
  //   styleUrls: ['./sign-up.component.css'],
})
export class SignUpComponent {
  form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    username: ['', [Validators.required, Validators.pattern(/^[a-zA-Z0-9]+$/)]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });
  constructor(private fb: FormBuilder) {}
  onSubmit() {
    if (this.form.valid) {
      console.log('Sign Up Data:', this.form.value);
    } else {
      this.form.markAllAsTouched();
    }
  }
}
