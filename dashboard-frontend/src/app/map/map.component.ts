import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { select, json, geoPath, geoMercator } from 'd3';
import { feature } from 'topojson-client';
import { CovidDataService } from '../services/covid-data.service';
import { Region } from '../models/region';
import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {
  private svg;
  private width = 900;
  private height = 600;
  private saudiTopoJson;
  regions: Region[];

  // private projection = geoMercator().scale(1).translate([this.width / 2, this.height / 2]);
  // private pathGenerator = geoPath().projection(this.projection);

  constructor(
    private http: HttpClient,
    private covidService: CovidDataService
  ) { }

  ngOnInit(): void {
    this.covidService.regions.subscribe((regions: Region[]) => {
      if (regions.length) {
        this.regions = regions;

        json('assets/saudi-arabia-topo.json').then((data: any) => {
          this.saudiTopoJson = data;
          this.appendCasesData();
          this.createMap();
        });
      }
    });
  }

  // Append all case data per region to topojson properties
  appendCasesData(): void {
    this.saudiTopoJson.objects.gadm36_SAU_1.geometries.map(r => {
      const region = this.regions.find(el => el.name === r.properties.NAME_1);
      r.properties.confirmed = region.confirmed;
      r.properties.active = region.active;
      r.properties.recoveries = region.recoveries;
      r.properties.deceased = region.mortalities;

      return r;
    });
  }

  createMap(): void {
    // const regions = feature(data, data.objects.gadm36_SAU_1);

    // const projection = geoMercator();
    // const pathGenerator = geoPath().projection(projection);

    // const g = this.svg.append('g')
    //   .attr('translate', `transform(${this.width / 2}, ${this.height / 2})`);

    // g.selectAll('path')
    //   .data(regions.features)
    //   .enter().append('path')
    //   .attr('d', pathGenerator);

  }
}
