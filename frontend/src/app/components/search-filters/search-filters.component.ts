import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

import { PropertyFilters, PropertyType, PropertyStatus } from '../../models/property';

@Component({
  selector: 'app-search-filters',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule
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
    this.form = this.fb.group<PropertyFilters>({
      city: this.fb.control(''),
      property_type: this.fb.control<PropertyType | ''>(''),
      status: this.fb.control<PropertyStatus | ''>(''),
      min_price: this.fb.control<number | null>(null),
      max_price: this.fb.control<number | null>(null),
      bedrooms: this.fb.control<number | null>(null),
      bathrooms: this.fb.control<number | null>(null)
    });
  }

  ngOnChanges(): void {
    if (this.initialFilters) {
      this.form.patchValue(this.initialFilters, { emitEvent: false });
    }
  }

  submit(): void {
    this.filterChange.emit({
      ...this.form.getRawValue(),
      property_type: this.form.value.property_type || undefined,
      status: this.form.value.status || undefined
    });
  }

  reset(): void {
    this.form.reset();
    this.filterChange.emit({});
  }
}
