import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Total } from '../models/total';
import { environment } from 'src/environments/environment';
import { Observable, Subject, BehaviorSubject } from 'rxjs';
import { Region } from '../models/region';
import { City } from '../models/city';

const baseURL = environment.baseURL;

@Injectable({
  providedIn: 'root'
})
export class CovidDataService {

  private _regions: BehaviorSubject<Region[]> = new BehaviorSubject<Region[]>([]);
  private _cities: BehaviorSubject<City[]> = new BehaviorSubject<City[]>([]);
  private _total: BehaviorSubject<Total> = new BehaviorSubject<Total>(null);

  public readonly regions = this._regions.asObservable();
  public readonly cities = this._cities.asObservable();
  public readonly total = this._total.asObservable();

  constructor(private http: HttpClient) {
    this.getTotal();
    this.getRegions();
  }

  getTotal(): void {
    this.http.get<Total>(`${baseURL}/total`).subscribe(total =>
      this._total.next(total[0])
    );
  }

  getRegions(): void {
    this.http.get<Region[]>(`${baseURL}/all-regions`).subscribe(regions =>
      this._regions.next(regions)
    );
  }

  getCities(): Observable<City[]> {
    return this.http.get<City[]>(`${baseURL}/all-cities`);
  }

}
