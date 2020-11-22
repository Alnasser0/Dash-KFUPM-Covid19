import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Total } from '../models/total';
import { environment } from 'src/environments/environment';
import { Observable, BehaviorSubject, pipe } from 'rxjs';
import { map } from 'rxjs/operators';
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
    this.http.get<Total>(`${baseURL}/total`).pipe(
      map(total => new Total(
        total[0].confirmed,
        total[0].active,
        total[0].recoveries,
        total[0].mortalities,
        total[0].critical,
        total[0].tested,
        total[0].population,
        total[0].daily,
        total[0].cumulative
      ))
    ).subscribe(total => {
      this._total.next(total);
    });
  }

  getRegions(): void {
    this.http.get<Region[]>(`${baseURL}/all-regions`).subscribe(regions => {
      regions = regions.map(region => new Region(
        region.name,
        region.confirmed,
        region.active,
        region.recoveries,
        region.mortalities,
        region.daily,
        region.cumulative,
        region.cities
      ));
      this._regions.next(regions);
    });
  }

  getCities(): Observable<City[]> {
    return this.http.get<City[]>(`${baseURL}/all-cities`);
  }

}
