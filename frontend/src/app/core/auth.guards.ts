import { Injectable } from '@angular/core';
import { URLS } from './routes/PATHS';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router,
  CanActivateChild,
} from '@angular/router';
import { AuthService } from './auth.service';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate, CanActivateChild {
  constructor(private authService: AuthService, private router: Router) {}

  // i need to protect both parent and all child
  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    return this.checkAccess(route);
  }

  canActivateChild(
    childRoute: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    return this.checkAccess(childRoute);
  }

  private checkAccess(route: ActivatedRouteSnapshot): boolean {
    const loggedInUsername = this.authService.getUsernameFromToken();
    const requestedUsername = route.params['userUsername'];

    if (
      this.authService.isAuthenticated() &&
      loggedInUsername === requestedUsername
    ) {
      return true;
    }
    if (loggedInUsername !== requestedUsername) {
      this.router.navigate([URLS.PUBLIC.USER_SHOP(requestedUsername)]);
      console.log(loggedInUsername, requestedUsername);
      return false;
    }

    this.router.navigate([URLS.PUBLIC.SIGN_IN]);
    return false;
  }
}
