import { Routes } from '@angular/router';

import { HomePageComponent } from './pages/home-page/home-page.component';
import { PropertyDetailsPageComponent } from './pages/property-details-page/property-details-page.component';
import { FavoritesPageComponent } from './pages/favorites-page/favorites-page.component';

export const routes: Routes = [
  { path: '', component: HomePageComponent },
  { path: 'properties/:id', component: PropertyDetailsPageComponent },
  { path: 'favorites', component: FavoritesPageComponent },
  { path: '**', redirectTo: '' }
];
