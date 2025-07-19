import 'zone.js';
import { bootstrapApplication } from '@angular/platform-browser';
// import { appConfig } from './app/app.config';
// bootstrapApplication(AppComponent, appConfig);

import { provideRouter } from '@angular/router';
import { importProvidersFrom } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { routes } from './app/routes/app.routes';
import { AppComponent } from './app/app.component';

// controls style import
import './styles.scss';

bootstrapApplication(AppComponent, {
  providers: [provideRouter(routes), importProvidersFrom(ReactiveFormsModule)],
});
