import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatIconModule } from '@angular/material/icon';
import { TitleCasePipe, NgFor } from '@angular/common';

import { PropertyFilters, PropertyType, PropertyStatus } from '../../models/property';

@Component({
  selector: 'app-search-filters',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatIconModule,
    TitleCasePipe,
    NgFor
  ],
  templateUrl: './search-filters.component.html',
  styleUrls: ['./search-filters.component.scss']
})
export class SearchFiltersComponent {
  @Input() initialFilters: PropertyFilters | null = null;
  @Output() filterChange = new EventEmitter<PropertyFilters>();

  readonly propertyTypes: PropertyType[] = ['apartment', 'house', 'land', 'commercial'];
  readonly propertyStatuses: PropertyStatus[] = ['available', 'pending', 'sold', 'rented'];

  form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      city: [''],
      property_type: [''],
      status: [''],
      min_price: [null],
      max_price: [null],
      bedrooms: [null],
      bathrooms: [null]
    });
  }

  ngOnChanges(): void {
    if (this.initialFilters) {
      this.form.patchValue(this.initialFilters, { emitEvent: false });
    }
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

  submit(): void {
    const formValue = this.form.getRawValue();
    this.filterChange.emit({
      ...formValue,
      property_type: formValue.property_type || undefined,
      status: formValue.status || undefined
    });
  }

  reset(): void {
    this.form.reset();
    this.filterChange.emit({});
  }
}