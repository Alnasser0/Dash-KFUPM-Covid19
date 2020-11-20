import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import {
  select,
  json,
  geoPath,
  geoMercator,
  geoCentroid,
  zoom,
  max,
  min,
  scaleQuantize,
  scaleThreshold,
  scaleLinear,
  scaleQuantile,
  schemeBlues,
  interpolateBlues,
  interpolateReds,
  scaleSequentialLog,
  scaleSequential,
} from 'd3';
import { feature } from 'topojson-client';
import { CovidDataService } from '../services/covid-data.service';
import { Region } from '../models/region';


// const COLORS = ['#6EE3FF', '#3BB0FF', '#2196F3'];

const COLORS = ['#FFEAF3', '#FFD0D9', '#FFB7C0', '#FF848D', '#FF9EA7', '#FF6B74', '#E7515A'];

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {

  private saudiTopoJson;
  regions: Region[];

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
          this.renderMap();
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

  renderMap(): void {
    const geojson = feature(this.saudiTopoJson, this.saudiTopoJson.objects.gadm36_SAU_1);

    const maxVal = +max(geojson.features, (d: any) => d.properties.confirmed);
    const minVal = +min(geojson.features, (d: any) => d.properties.confirmed);

    const color = scaleSequentialLog()
      .domain([minVal, maxVal])
      .interpolator(interpolateBlues);

    const svg = select('svg').attr('viewBox', `0 0 600 500`);
    const width = +svg.attr('width');
    const height = +svg.attr('height');

    const center = geoCentroid(geojson);

    const projection = geoMercator().scale(1500).center(center).translate([width / 2, height / 2]);
    const pathGenerator = geoPath().projection(projection);

    const map = svg.append('g');

    map.selectAll('path')
      .data(geojson.features)
      .enter().append('path')
      .attr('class', 'region')
      .attr('fill', (d: any) => color(d.properties.confirmed))
      .attr('d', pathGenerator);

    svg.call(zoom().on('zoom', event => {
      map.attr('transform', event.transform);
    }));
  }
}
