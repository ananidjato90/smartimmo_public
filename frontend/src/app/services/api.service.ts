import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { Property, PropertyFilters } from '../models/property';
import { Favorite } from '../models/favorite';
import { User } from '../models/user';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly baseUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getProperties(filters: PropertyFilters = {}): Observable<Property[]> {
    let params = new HttpParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params = params.set(key, value as string);
      }
    });
    return this.http.get<Property[]>(`${this.baseUrl}/properties`, { params });
  }

  getProperty(id: number): Observable<Property> {
    return this.http.get<Property>(`${this.baseUrl}/properties/${id}`);
  }

  createProperty(property: Partial<Property>): Observable<Property> {
    return this.http.post<Property>(`${this.baseUrl}/properties`, property);
  }

  updateProperty(id: number, property: Partial<Property>): Observable<Property> {
    return this.http.put<Property>(`${this.baseUrl}/properties/${id}`, property);
  }

  deleteProperty(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/properties/${id}`);
  }

  listFavorites(): Observable<Favorite[]> {
    return this.http.get<Favorite[]>(`${this.baseUrl}/favorites`);
  }

  addFavorite(propertyId: number): Observable<Favorite> {
    return this.http.post<Favorite>(`${this.baseUrl}/favorites/${propertyId}`, {});
  }

  removeFavorite(propertyId: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/favorites/${propertyId}`);
  }

  register(user: Partial<User> & { password: string }): Observable<User> {
    return this.http.post<User>(`${this.baseUrl}/users`, user);
  }

  login(credentials: { email: string; password: string }): Observable<User> {
    return this.http.post<User>(`${this.baseUrl}/users/login`, credentials);
  }
}
