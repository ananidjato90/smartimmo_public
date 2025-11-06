import { Component, EventEmitter, Input, Output } from '@angular/core';
import { NgIf, CurrencyPipe, SlicePipe } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { RouterModule } from '@angular/router';

import { Property, PropertyType, PropertyStatus } from '../../models/property';

@Component({
  selector: 'app-property-card',
  standalone: true,
  imports: [
    MatCardModule, 
    MatButtonModule, 
    MatIconModule,
    RouterModule, 
    NgIf, 
    CurrencyPipe, 
    SlicePipe
  ],
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

  getPropertyTypeLabel(type: PropertyType): string {
    const labels: Record<PropertyType, string> = {
      'apartment': 'Appartement',
      'house': 'Maison',
      'land': 'Terrain',
      'commercial': 'Commercial'
    };
    return labels[type] || type;
  }

  getStatusLabel(status: PropertyStatus): string {
    const labels: Record<PropertyStatus, string> = {
      'available': 'Disponible',
      'pending': 'En attente',
      'sold': 'Vendu',
      'rented': 'Loué'
    };
    return labels[status] || status;
  }

  toggleFavorite(): void {
    this.favoriteToggle.emit(this.property);
  }
}