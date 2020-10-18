import { Component, OnInit } from '@angular/core';
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
  }

  getCities(): void {
    this.covidDataService.getAllCities().subscribe(cities => {
      for (const city of cities) {
        this.allCiites[city.name] = city;
      }
      this.updateCities();
      this.isCitiesLoaded = true;
    });
  }

  getRegions(): void {
    this.covidDataService.getAllRegions().subscribe(regions => {
      this.allRegions['All Regions'] = {};

      for (const region of regions) {
        this.allRegions[region.name] = region;
      }

      this.isRegionsLoaded = true;

      this.regionNames = Object.keys(this.allRegions);
    });
  }

  updateCities(): void {
    let cities = [];
    this.selectedCities = [];

    if (this.selectedRegion === 'All Regions') {
      this.selectedCities = Object.values(this.allCiites);
    } else {
      cities = this.allRegions[this.selectedRegion].cities;

      for (const city of cities) {
        this.selectedCities.push(this.allCiites[city]);
      }
    }

    this.selectedCities.sort((a, b) => b.confirmed - a.confirmed);

    console.log(this.selectedCities);
  }
}
