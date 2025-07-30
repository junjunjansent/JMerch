import { Injectable, inject } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({ providedIn: 'root' })
export class SnackBarService {
  constructor(private snackBar: MatSnackBar) {}

  info(message: string, action: string = 'Close', duration: number = 5) {
    return this.snackBar.open(message, action, {
      panelClass: ['snackbar-info'],
      duration: duration * 1000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
      politeness: 'assertive',
    });
  }

  success(message: string, action: string = 'Close', duration: number = 5) {
    return this.snackBar.open(message, action, {
      panelClass: ['snackbar-success'],
      duration: duration * 1000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
    });
  }

  error(message: string, action: string = 'Close', duration: number = 5) {
    return this.snackBar.open(message, action, {
      panelClass: ['snackbar-error'],
      duration: duration * 1000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
    });
  }
}
