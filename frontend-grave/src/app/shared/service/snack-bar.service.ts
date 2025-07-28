import { Injectable, inject } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';

@Injectable({ providedIn: 'root' })
export class SnackBarService {
  private _snackBar = inject(MatSnackBar);

  success(message: string, action: string = 'Close', duration: number = 5) {
    return this._snackBar.open(message, action, {
      panelClass: ['snackbar-success'],
      duration: duration * 1000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
    });
  }

  error(message: string, action: string = 'Close', duration: number = 5) {
    return this._snackBar.open(message, action, {
      panelClass: ['snackbar-error'],
      duration: duration * 1000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
    });
  }

  info(message: string, action: string = 'Close', duration: number = 5) {
    return this._snackBar.open(message, action, {
      panelClass: ['snackbar-info'],
      duration: duration * 1000,
      horizontalPosition: 'right',
      verticalPosition: 'top',
    });
  }
}
