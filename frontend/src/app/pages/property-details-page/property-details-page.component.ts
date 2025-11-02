import { Component, OnDestroy } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { CommonModule, CurrencyPipe, DatePipe } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Subscription, switchMap } from 'rxjs';

import { ApiService } from '../../services/api.service';
import { Property } from '../../models/property';

@Component({
  selector: 'app-property-details-page',
  standalone: true,
  imports: [CommonModule, RouterModule, MatButtonModule, MatIconModule, CurrencyPipe, DatePipe],
  templateUrl: './property-details-page.component.html',
  styleUrls: ['./property-details-page.component.scss']
})
export class PropertyDetailsPageComponent implements OnDestroy {
  property?: Property;
  private subscription?: Subscription;

  constructor(private route: ActivatedRoute, private api: ApiService) {
    this.subscription = this.route.paramMap
      .pipe(
        switchMap((params) => {
          const id = Number(params.get('id'));
          return this.api.getProperty(id);
        })
      )
      .subscribe((property) => (this.property = property));
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }
}
