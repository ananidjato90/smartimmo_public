export type PropertyStatus = 'available' | 'pending' | 'sold' | 'rented';
export type PropertyType = 'apartment' | 'house' | 'land' | 'commercial';

export interface PropertyImage {
  id?: number;
  url: string;
  is_primary?: boolean;
}

export interface Property {
  id: number;
  title: string;
  description: string;
  price: number;
  area?: number;
  bedrooms?: number;
  bathrooms?: number;
  city: string;
  district?: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  property_type: PropertyType;
  status: PropertyStatus;
  is_featured: boolean;
  owner_id: number;
  created_at: string;
  updated_at: string;
  images: PropertyImage[];
}

export interface PropertyFilters {
  city?: string;
  property_type?: PropertyType;
  status?: PropertyStatus;
  min_price?: number;
  max_price?: number;
  bedrooms?: number;
  bathrooms?: number;
  is_featured?: boolean;
}
