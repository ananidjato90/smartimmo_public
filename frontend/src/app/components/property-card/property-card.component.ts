import { Component, EventEmitter, Input, Output } from '@angular/core';
import { NgIf, NgFor, CurrencyPipe, DatePipe } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { RouterModule } from '@angular/router';

import { Property } from '../../models/property';

@Component({
  selector: 'app-property-card',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, RouterModule, NgIf, NgFor, CurrencyPipe, DatePipe],
  templateUrl: './property-card.component.html',
  styleUrls: ['./property-card.component.scss']
})
export class PropertyCardComponent {
  @Input({ required: true }) property!: Property;
  @Input() isFavorite = false;
  @Output() favoriteToggle = new EventEmitter<Property>();

  get primaryImage(): string {
    const featured = this.property.images?.find((img) => img.is_primary);
    return featured?.url || this.property.images?.[0]?.url || 'https://placehold.co/600x400?text=SmartImmo';
  }

  toggleFavorite(): void {
    this.favoriteToggle.emit(this.property);
  }
}
