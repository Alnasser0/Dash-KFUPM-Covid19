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
  @Output() selectCityEvent = new EventEmitter<City>();
  @Output() selectRegionEvent = new EventEmitter<Region>();
  @Output() selectTotalEvent = new EventEmitter<Total>();
  @Output() showTotalEvent = new EventEmitter<boolean>();

  regions: Region[];
  isRegionsLoaded = false;

  constructor(private covidDataService: CovidDataService) { }

  ngOnInit(): void {
    this.getRegions();
  }

  getRegions(): void {
    this.covidDataService.regions.subscribe((regions: Region[]) => {
      if (regions.length) {
        this.regions = regions;
        this.regions.sort((a, b) => +b.confirmed - +a.confirmed);
        this.isRegionsLoaded = true;
      }
    });
  }
}
