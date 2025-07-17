import { Routes } from '@angular/router';
import { HomeComponent } from '../pages/public/home.component';
import { SignUpComponent } from '../pages/public/sign-up.component';
import { SignInComponent } from '../pages/public/sign-in.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'sign-up', component: SignUpComponent },
  { path: 'sign-in', component: SignInComponent },
];
