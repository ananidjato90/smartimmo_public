import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

import { ApiService } from '../../services/api.service';
import { Favorite } from '../../models/favorite';
import { PropertyCardComponent } from '../../components/property-card/property-card.component';

@Component({
  selector: 'app-favorites-page',
  standalone: true,
  imports: [CommonModule, MatSnackBarModule, PropertyCardComponent],
  templateUrl: './favorites-page.component.html',
  styleUrls: ['./favorites-page.component.scss']
})
export class FavoritesPageComponent implements OnInit {
  favorites: Favorite[] = [];

  constructor(private api: ApiService, private snackBar: MatSnackBar) {}

  ngOnInit(): void {
    this.loadFavorites();
  }

  loadFavorites(): void {
    this.api.listFavorites().subscribe({
      next: (favorites) => (this.favorites = favorites),
      error: () =>
        this.snackBar.open('Impossible de charger vos favoris', 'Fermer', {
          duration: 3000
        })
    });
  }

  removeFavorite(propertyId: number): void {
    this.api.removeFavorite(propertyId).subscribe({
      next: () => {
        this.favorites = this.favorites.filter((fav) => fav.property.id !== propertyId);
        this.snackBar.open('Favori retir?', undefined, { duration: 2000 });
      },
      error: () => {
        this.snackBar.open('Impossible de retirer ce favori', 'Fermer', {
          duration: 3000
        });
      }
    });
  }
}
