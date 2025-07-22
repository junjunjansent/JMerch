import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { type UserProfile } from '../types/user';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private baseUserURL = `${import.meta.env['VITE_DEV_BASE_URL']}/users`;
  private ownerURL = `${this.baseUserURL}/owner`;
  private ownerPasswordURL = `${this.ownerURL}/password`;

  constructor(private http: HttpClient) {}

  showOwnerProfile(): Observable<{ user: UserProfile }> {
    return this.http.get<{ user: UserProfile }>(this.ownerURL);
  }
}
