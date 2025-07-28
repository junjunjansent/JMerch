// import 'zone.js';
// import { bootstrapApplication } from '@angular/platform-browser';
// // import { appConfig } from './app/app.config';
// // bootstrapApplication(AppComponent, appConfig);

import 'zone.js';
import { bootstrapApplication } from '@angular/platform-browser';

import { provideRouter } from '@angular/router';
import { routes } from './app/routes/app.routes';
import { importProvidersFrom } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
// import { authInterceptor } from './app/core/auth.interceptor';

import { AppComponent } from './app/app.component';
// controls style import
import './assets/styles/styles.scss';

bootstrapApplication(AppComponent, {
  providers: [
    importProvidersFrom(ReactiveFormsModule),
    provideRouter(routes),
    // provideHttpClient(withInterceptors([authInterceptor])), //use function based interceptor (newer) in the end, safer with Angular 15+, class-based more for NgModule
  ],
});
