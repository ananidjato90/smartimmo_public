import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { finalize } from 'rxjs/operators';

import { Property, PropertyFilters } from '../../models/property';
import { ApiService } from '../../services/api.service';
import { AiAgentService } from '../../services/ai-agent.service';
import { PropertyCardComponent } from '../../components/property-card/property-card.component';
import { SearchFiltersComponent } from '../../components/search-filters/search-filters.component';
import { AiAssistantPanelComponent } from '../../components/ai-assistant-panel/ai-assistant-panel.component';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    CommonModule,
    MatSnackBarModule,
    PropertyCardComponent,
    SearchFiltersComponent,
    AiAssistantPanelComponent
  ],
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss']
})
export class HomePageComponent {
  properties: Property[] = [];
  filters: PropertyFilters = {};
  favorites = new Set<number>();

  constructor(
    private api: ApiService,
    private ai: AiAgentService,
    private snackBar: MatSnackBar
  ) {
    this.loadProperties();
    this.loadFavorites();
  }

  loadProperties(): void {
    this.api.getProperties(this.filters).subscribe({
      next: (properties) => {
        this.properties = properties;
      },
      error: () => {
        this.snackBar.open('Impossible de charger les propriétés', 'Fermer', {
          duration: 3000
        });
      }
    });
  }

  loadFavorites(): void {
    this.api.listFavorites().subscribe({
      next: (favorites) => {
        this.favorites = new Set(favorites.map((fav) => fav.property.id));
      },
      error: () => {
        this.favorites.clear();
      }
    });
  }

  onFiltersChange(filters: PropertyFilters): void {
    this.filters = filters;
    this.loadProperties();
  }

  toggleFavorite(property: Property): void {
    const isFavorite = this.favorites.has(property.id);
    
    if (isFavorite) {
      this.api.removeFavorite(property.id).subscribe({
        next: () => {
          this.favorites.delete(property.id);
          this.snackBar.open('Retiré des favoris', undefined, { duration: 2000 });
        },
        error: () => {
          this.snackBar.open('Action indisponible. Vérifiez votre session.', 'Fermer', {
            duration: 3000
          });
        }
      });
    } else {
      this.api.addFavorite(property.id).subscribe({
        next: () => {
          this.favorites.add(property.id);
          this.snackBar.open('Ajouté aux favoris', undefined, { duration: 2000 });
        },
        error: () => {
          this.snackBar.open('Action indisponible. Vérifiez votre session.', 'Fermer', {
            duration: 3000
          });
        }
      });
    }
  }

  handleAgentQuery(component: AiAssistantPanelComponent, prompt: string): void {
    component.setLoading(true);
    this.ai.ask(prompt).subscribe({
      next: (res) => component.setResponse(res.response),
      error: () => {
        component.setResponse("L'assistant est indisponible pour le moment.");
        this.snackBar.open("Erreur lors de la consultation de l'assistant", 'Fermer', {
          duration: 3000
        });
      }
    });
  }
}