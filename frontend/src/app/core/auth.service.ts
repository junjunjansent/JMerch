import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { SnackBarService } from '../shared/service/snack-bar.service';

interface SignUpData {
  username: string;
  email: string;
  password: string;
}

interface SignInData {
  usernameOrEmail: string;
  password: string;
}

interface AuthResponse {
  token: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  // Observable reactive state!
  private authState$ = new BehaviorSubject<boolean>(this.isAuthenticated());

  private baseURL = `${import.meta.env['VITE_DEV_BASE_URL']}/public`;
  private signUpURL = `${this.baseURL}/sign-up`;
  private signInURL = `${this.baseURL}/sign-in`;

  constructor(private http: HttpClient, private snackBar: SnackBarService) {}

  private getToken(): string | null {
    return localStorage.getItem('token');
  }

  // this is the one that reactively tracks and for me to read the state
  isLoggedIn$ = this.authState$.asObservable();

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  getUsernameFromToken(): string {
    const token = this.getToken();
    if (token) {
      const userInfo = JSON.parse(atob(token.split('.')[1]));
      return userInfo.username;
    } else {
      this.snackBar.error('No Token Found');
      localStorage.removeItem('token');
      return '';
    }
  }

  signUp(signUpData: SignUpData): Observable<AuthResponse> {
    return this.http
      .post<{ token: string }>(`${this.signUpURL}`, signUpData)
      .pipe(
        tap((response) => {
          localStorage.setItem('token', response.token);
          this.authState$.next(true); // because i need to update the observable state})));
        })
      );
  }

  signIn(signInData: SignInData): Observable<AuthResponse> {
    return this.http
      .post<{ token: string }>(`${this.signInURL}`, signInData)
      .pipe(
        tap((response) => {
          localStorage.setItem('token', response.token);
          this.authState$.next(true); // because i need to update the observable state})));
        })
      );
  }

  signOut(): void {
    localStorage.removeItem('token');
    this.authState$.next(false); // because i need to update the observable state
  }
}
