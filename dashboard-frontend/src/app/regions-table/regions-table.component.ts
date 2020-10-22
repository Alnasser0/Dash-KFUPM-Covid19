import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { City } from '../models/city';
import { Region } from '../models/region';
import { Total } from '../models/total';
import { CovidDataService } from '../services/covid-data.service';

@Component({
  selector: 'app-regions-table',
  templateUrl: './regions-table.component.html',
  styleUrls: ['./regions-table.component.scss']
})
export class RegionsTableComponent implements OnInit {
  displayRegions = false;
  defaultRegion = 'Eastern Region';
  selectedRegion = this.defaultRegion;
  total: Total;

  @Output() selectCityEvent = new EventEmitter<City>();
  @Output() selectRegionEvent = new EventEmitter<Region>();
  @Output() selectTotalEvent = new EventEmitter<Total>();
  @Output() showTotalEvent = new EventEmitter<boolean>();

  allRegions = {};
  allCiites = {};

  regionNames = [];
  selectedCities = [];

  isCitiesLoaded = false;
  isRegionsLoaded = false;

  constructor(private covidDataService: CovidDataService) { }

  ngOnInit(): void {
    this.getCities();
    this.getRegions();
    this.getTotal();
  }

  getCities(): void {
    this.covidDataService.getAllCities().subscribe((cities: City[]) => {
      for (const city of cities) {
        this.allCiites[city.name] = city;
      }
      this.updateCities();
      this.isCitiesLoaded = true;
    });
  }

  getRegions(): void {
    this.covidDataService.getAllRegions().subscribe((regions: Region[]) => {
      this.allRegions['All Regions'] = {};

      for (const region of regions) {
        this.allRegions[region.name] = region;
      }

      this.isRegionsLoaded = true;

      this.regionNames = Object.keys(this.allRegions);
    });
  }

  getTotal(): void {
    this.covidDataService.getTotal().subscribe((total: Total) => {
      this.total = total[0];
    });
  }

  updateCities(): void {
    let cities = [];
    this.selectedCities = [];

    if (this.selectedRegion === 'All Regions') {
      this.selectedCities = Object.values(this.allCiites);
      this.selectTotal(this.total);
      this.showTotal(true);
    } else {
      cities = this.allRegions[this.selectedRegion].cities;

      for (const city of cities) {
        this.selectedCities.push(this.allCiites[city]);
      }


      const region = this.allRegions[this.selectedRegion];
      this.selectRegion(region);
      this.showTotal(false);
    }

    this.selectedCities.sort((a, b) => b.confirmed - a.confirmed);
    this.selectCity(this.selectedCities[0]);
  }

  selectCity(city: City): void {
    this.selectCityEvent.emit(city);
  }

  selectRegion(region: Region): void {
    this.selectRegionEvent.emit(region);
  }

  selectTotal(total: Total): void {
    this.selectTotalEvent.emit(total);
  }

  showTotal(flag: boolean): void {
    this.showTotalEvent.emit(flag);
  }
}
