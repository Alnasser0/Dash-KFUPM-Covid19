import { Component, OnInit } from '@angular/core';

import {
  select,
  json,
  geoPath,
  geoMercator,
  geoCentroid,
  zoom,
  max,
  min,
  interpolateBlues,
  interpolateReds,
  interpolateOrRd,
  scaleSequential
} from 'd3';

import { feature } from 'topojson-client';
import { Region } from 'src/app/models/region';
import { CovidDataService } from 'src/app/services/covid-data.service';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {

  private saudiTopoJson;
  regions: Region[];
  population = 0;
  lastUpdated = '';

  constructor(
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

    this.covidService.total.subscribe(total => {
      if (total) {
        this.population = total.population;
        const lastDate = total.daily[total.daily.length - 1]['Date'];
        const d = new Date(lastDate);

        const months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December'];

        const month = months[d.getMonth()];

        this.lastUpdated = `${d.getDate()} ${month} ${d.getFullYear()}, 5:00 PM AST`;
      }
    });
  }

  // Append all case data per region to topojson properties
  appendCasesData(): void {
    this.saudiTopoJson.objects.regions.geometries.map(r => {
      const region = this.regions.find(el => el.name === r.properties.name);
      r.properties.confirmed = region.confirmed;
      r.properties.active = region.active;
      r.properties.recoveries = region.recoveries;
      r.properties.deceased = region.mortalities;

      return r;
    });
  }

  renderMap(): void {
    const geojson = feature(this.saudiTopoJson, this.saudiTopoJson.objects.regions);

    const maxVal = +max(geojson.features, (d: any) => d.properties.confirmed);
    const minVal = +min(geojson.features, (d: any) => d.properties.confirmed);

    const color = scaleSequential()
      .domain([minVal, maxVal])
      .interpolator(interpolateBlues);

    const svg = select('svg').attr('viewBox', `0 0 650 650`);
    const width = +svg.attr('width');
    const height = +svg.attr('height');

    // svg.append('g')
    //   .append(() => legend({ color, title: 'Confirmed cases' }));

    const center = geoCentroid(geojson);

    const projection = geoMercator().scale(1700).center(center).translate([width / 2, height / 2]);
    const pathGenerator = geoPath().projection(projection);

    const map = svg.append('g');

    map.selectAll('path')
      .data(geojson.features)
      .enter().append('path')
      .attr('class', 'region')
      .attr('fill', (d: any) => color(d.properties.confirmed))
      .attr('d', pathGenerator);

    // svg.call(zoom().on('zoom', event => {
    //   map.attr('transform', event.transform);
    // }));

  }
}
