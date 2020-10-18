import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Total } from '../models/total';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';
import { Region } from '../models/region';
import { City } from '../models/city';

const baseURL = environment.baseURL;

@Injectable({
  providedIn: 'root'
})
export class CovidDataService {
  total: Total;
  regions: Region[] = [];
  cities: City[] = [];

  selectedRegion: Region;
  selectedCity: City;

  constructor(private http: HttpClient) { }

  getTotal(): Observable<Total> {
    return this.http.get<Total>(`${baseURL}/total`);
  }

  getAllRegions(): Observable<Region[]> {
    return this.http.get<Region[]>(`${baseURL}/all-regions`);
  }

  getAllCities(): Observable<City[]> {
    return this.http.get<City[]>(`${baseURL}/all-cities`);
  }

}
