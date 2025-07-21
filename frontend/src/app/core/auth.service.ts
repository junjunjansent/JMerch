import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
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
  private baseURL = `${import.meta.env['VITE_DEV_BASE_URL']}/public`;
  private signUpURL = `${this.baseURL}/sign-up`;
  private signInURL = `${this.baseURL}/sign-in`;

  constructor(private http: HttpClient, private snackBar: SnackBarService) {}

  signUp(signUpData: SignUpData): Observable<AuthResponse> {
    return this.http
      .post<{ token: string }>(`${this.signUpURL}`, signUpData)
      .pipe(tap((response) => localStorage.setItem('token', response.token)));
  }

  signIn(signInData: SignInData): Observable<AuthResponse> {
    return this.http
      .post<{ token: string }>(`${this.signInURL}`, signInData)
      .pipe(tap((response) => localStorage.setItem('token', response.token)));
  }

  signOut(): void {
    localStorage.removeItem('token');
  }

  getToken(): string | null {
    const token = localStorage.getItem('token');
    if (token) {
      return token;
    } else {
      this.snackBar.error('No Token Found');
      localStorage.removeItem('token');
      //   throw new Error('No Token Found');
      return null;
    }
  }

  getUsernameFromToken(): string | null {
    const token = localStorage.getItem('token');
    if (token) {
      const userInfo = JSON.parse(atob(token.split('.')[1]));
      return userInfo.username;
    } else {
      this.snackBar.error('No Token Found');
      localStorage.removeItem('token');
      throw new Error('No Token Found');
    }
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}
