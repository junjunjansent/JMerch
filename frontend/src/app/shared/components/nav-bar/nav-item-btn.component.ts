import { Component, Input } from '@angular/core';

import { RouterModule } from '@angular/router';

import { MatButtonModule } from '@angular/material/button';
import { MatMenu, MatMenuModule } from '@angular/material/menu';

@Component({
  selector: 'nav-item-btn',
  standalone: true,
  imports: [RouterModule, MatButtonModule, MatMenuModule], // for routeLink & routeActive
  templateUrl: './nav-item-btn.component.html',
})
export class NavItemBtnComponent {
  @Input() label!: string; //cannot be null
  @Input() to?: string;
  @Input() exactMatch = true;
  @Input() matMenuTriggerFor?: MatMenu;
}
