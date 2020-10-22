import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Label } from 'ng2-charts';
import { City } from '../models/city';
import { Region } from '../models/region';
import { Total } from '../models/total';

@Component({
  selector: 'app-charts',
  templateUrl: './charts.component.html',
  styleUrls: ['./charts.component.scss']
})
export class ChartsComponent implements OnInit, OnChanges {

  @Input() showTotal: boolean;

  @Input() region: Region;
  @Input() city: City;
  @Input() total: Total;

  public lineChartType = 'line';

  public regionCumulativeConfirmed: ChartDataSets[];
  public regionCumulativeActive: ChartDataSets[];
  public regionCumulativeRecovered: ChartDataSets[];
  public regionCumulativeMortalities: ChartDataSets[];

  public regionCumulativeLabels: Label[];

  public cityCumulativeConfirmed: ChartDataSets[];
  public cityCumulativeActive: ChartDataSets[];
  public cityCumulativeRecovered: ChartDataSets[];
  public cityCumulativeMortalities: ChartDataSets[];

  public cityCumulativeLabels: Label[];

  public confirmedChartOptions: ChartOptions = {
    responsive: true,
    title: {
      display: true,
      text: 'Confirmed'
    },
    legend: {
      display: false
    }
  };

  public activeChartOptions: ChartOptions = {
    responsive: true,
    title: {
      display: true,
      text: 'Active'
    },
    legend: {
      display: false
    }
  };

  public recoveriesChartOptions: ChartOptions = {
    responsive: true,
    title: {
      display: true,
      text: 'Recovered'
    },
    legend: {
      display: false
    }
  };

  public mortalitiesChartOptions: ChartOptions = {
    responsive: true,
    title: {
      display: true,
      text: 'Deceased'
    },
    legend: {
      display: false
    }
  };

  constructor() { }
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.region) {
      const cumulativeConfirmed = this.region.cumulative.map(c => c['Confirmed']);
      this.regionCumulativeConfirmed = [{ data: cumulativeConfirmed }];

      const cumulativeActive = this.region.cumulative.map(c => c['Active']);
      this.regionCumulativeActive = [{ data: cumulativeActive }];

      const cumulativeRecovered = this.region.cumulative.map(c => c['Recoveries']);
      this.regionCumulativeRecovered = [{ data: cumulativeRecovered }];

      const cumulativeMortalities = this.region.cumulative.map(c => c['Mortalities']);
      this.regionCumulativeMortalities = [{ data: cumulativeMortalities }];

      this.regionCumulativeLabels = this.region.cumulative.map(d => d['Date']);
    }

    if (changes.city) {
      const cumulativeConfirmed = this.city.cumulative.map(c => c['Confirmed']);
      this.cityCumulativeConfirmed = [{ data: cumulativeConfirmed }];

      const cumulativeActive = this.city.cumulative.map(c => c['Active']);
      this.cityCumulativeActive = [{ data: cumulativeActive }];

      const cumulativeRecovered = this.city.cumulative.map(c => c['Recoveries']);
      this.cityCumulativeRecovered = [{ data: cumulativeRecovered }];

      const cumulativeMortalities = this.city.cumulative.map(c => c['Mortalities']);
      this.cityCumulativeMortalities = [{ data: cumulativeMortalities }];

      this.cityCumulativeLabels = this.city.cumulative.map(d => d['Date']);
    }
  }

  ngOnInit(): void {
  }

}
