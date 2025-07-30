import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'info-text-card',
  standalone: true,
  imports: [CommonModule, MatCardModule],
  templateUrl: './info-text-card.component.html',
  // styleUrls: ['./info-text-card.component.scss'],
})
export class InfoTextCardComponent {
  @Input() label = '';
  @Input() value: string | number | null = null;
}
