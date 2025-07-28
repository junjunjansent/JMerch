import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'form-field-text',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
  ],
  templateUrl: './form-field-text.component.html',
})
export class FormFieldTextComponent {
  @Input() label!: string;
  @Input() type = 'text';
  @Input() required: boolean = false;
  @Input() control!: FormControl; //value and validation status
  @Input() autocomplete?: string;
  @Input() patternErrorMessage?: string;

  // getter method so
  get errorMessages(): string[] {
    const control = this.control; // compulsory from above
    const errors = control.errors; // object

    // dont show errors if user did not change the UI or touch the UI (for good UX)
    if (!errors || (!control.dirty && !control.touched)) return [];

    // want to only see if have errors of:
    // required, minlength, maxlength, pattern
    // give list of messages
    const messages: string[] = [];

    if (errors['required']) messages.push(`${this.label} is required`);
    if (errors['email'])
      messages.push(`${this.label} needs to be in valid email format`);
    if (errors['minlength'])
      messages.push(`Minimum ${errors['minlength'].requiredLength} characters`);
    if (errors['maxlength'])
      messages.push(`Maximum ${errors['maxlength'].requiredLength} characters`);
    if (errors['pattern'])
      messages.push(`${this.patternErrorMessage || 'InvalidFormat'}`);

    return messages;
  }
}
