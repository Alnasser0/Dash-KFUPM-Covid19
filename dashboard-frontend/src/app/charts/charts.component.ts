import { Component, Input, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { BaseChartDirective, Label } from 'ng2-charts';
import { Region } from '../models/region';
import { Total } from '../models/total';
import { CovidDataService } from '../services/covid-data.service';

@Component({
  selector: 'app-charts',
  templateUrl: './charts.component.html',
  styleUrls: ['./charts.component.scss']
})
export class ChartsComponent implements OnInit, OnChanges {

  // @Input() selectedRegion: Region;
  @ViewChild(BaseChartDirective) private _chart;

  regions: Region[];
  total: Total;

  isRefreshing = false;

  regionNames: string[];
  defaultRegion = 'Saudi Arabia';
  selectedRegion = this.defaultRegion;

  public lineChartType = 'line';

  displayMode = 'Daily';

  public confirmedLineChartData: ChartDataSets[];
  public activeLineChartData: ChartDataSets[];
  public recoveredLineChartData: ChartDataSets[];
  public deceasedLineChartData: ChartDataSets[];
  public testedLineChartData: ChartDataSets[];
  public criticalLineChartData: ChartDataSets[];

  public cumulativeLabels: Label[];

  public cumulativeOptions: ChartOptions = {
    responsive: true,
    elements: {
      point: {
        radius: 2
      }
    },
    legend: {
      display: false
    },
    tooltips: {
      intersect: false
    },
    hover: {
      intersect: false,
      animationDuration: 0
    },
    scales: {
      xAxes: [{
        type: 'time',
        distribution: 'linear',
        time: {
          unit: 'day'
        },
        ticks: {
          fontSize: 13,
          fontColor: 'rgba(255, 255, 255, 0.8)',
          maxTicksLimit: 10
        },
        gridLines: {
          drawOnChartArea: false,
          lineWidth: 1,
          color: 'rgba(255, 255, 255, 0.8)'
        }
      }],
      yAxes: [{
        ticks: {
          fontSize: 13,
          fontColor: 'rgba(255, 255, 255, 0.8)',
          callback: (value) => value.toLocaleString(),
          maxTicksLimit: 10
        },
        gridLines: {
          drawOnChartArea: false,
          lineWidth: 0.9,
          color: 'rgba(255, 255, 255, 0.8)'
        }
      }]
    }
  };

  constructor(private covidDataService: CovidDataService) { }

  ngOnChanges(changes: SimpleChanges): void {

  }

  ngOnInit(): void {
    this.getRegions();
    this.getTotal();
  }

  changeDisplayMode(mode: string): void {
    this.displayMode = mode;
    this.isRefreshing = true;

    switch (mode) {
      case 'daily': break;

      case 'cumulative':
        this.cumulativeOptions.scales.yAxes[0].type = 'linear';
        break;

      case 'log':
        this.cumulativeOptions.scales.yAxes[0].type = 'logarithmic';
        break;
    }

    setTimeout(() => {
      this.isRefreshing = false;
    }, 0);
  }

  getRegions(): void {
    this.covidDataService.regions.subscribe(regions => {
      if (regions.length > 0) {
        this.regions = regions;
        this.regionNames = this.regions.map(region => region.name);
        this.regionNames.unshift('Saudi Arabia');
        this.updateCharts();
      }
    });
  }

  getTotal(): void {
    this.covidDataService.total.subscribe(total => this.total = total);
  }

  updateCharts(): void {
    let newRegion;
    if (this.selectedRegion === 'Saudi Arabia') {
      newRegion = this.total;

      const cumulativeTested = newRegion.cumulative.map(c => c['Tested']);
      this.configTestedLineChart(cumulativeTested);

      const cumulativeCritical = newRegion.cumulative.map(c => c['Critical']);
      this.configCriticalLineChart(cumulativeCritical);
    } else {
      newRegion = this.regions.find(region => region.name === this.selectedRegion);
    }

    const cumulativeConfirmed = newRegion.cumulative.map(c => c['Confirmed']);
    this.configConfirmedLineChart(cumulativeConfirmed);

    const cumulativeActive = newRegion.cumulative.map(c => c['Active']);
    this.configActiveLineChart(cumulativeActive);

    const cumulativeRecovered = newRegion.cumulative.map(c => c['Recoveries']);
    this.configRecoveredLineChart(cumulativeRecovered)

    const cumulativeDeceased = newRegion.cumulative.map(c => c['Mortalities']);
    this.configDeceasedLineChart(cumulativeDeceased);

    this.cumulativeLabels = newRegion.cumulative.map(d => d['Date']);

  }

  configConfirmedLineChart(data): void {
    const confirmedLineChartOptions = {
      data,
      pointBorderWidth: 0.5,
      pointBorderColor: 'rgba(33,150,243, 0.9)',
      pointHoverBackgroundColor: 'rgba(33,150,243, 1)',
      pointHoverBorderColor: 'rgba(33,150,243, 1)',
      pointBackgroundColor: 'rgba(33,150,243, 1)',
      backgroundColor: 'rgba(33,150,243, 0.3)',
      borderColor: 'rgba(33,150,243, 1)'
    };
    this.confirmedLineChartData = [confirmedLineChartOptions];
  }

  configActiveLineChart(data): void {
    const activeLineChartOptions = {
      data,
      pointBorderWidth: 0.5,
      pointBorderColor: 'rgba(231,81,90, 0.9)',
      pointHoverBackgroundColor: 'rgba(231,81,90, 1)',
      pointHoverBorderColor: 'rgba(231,81,90, 1)',
      pointBackgroundColor: 'rgba(231,81,90, 1)',
      backgroundColor: 'rgba(231,81,90, 0.3)',
      borderColor: 'rgba(231,81,90, 1)'
    };
    this.activeLineChartData = [activeLineChartOptions];
  }

  configRecoveredLineChart(data): void {
    const recoverdLineChartOptions = {
      data,
      pointBorderWidth: 0.5,
      pointBorderColor: 'rgba(141,191,66, 0.9)',
      pointHoverBackgroundColor: 'rgba(141,191,66, 1)',
      pointHoverBorderColor: 'rgba(141,191,66, 1)',
      pointBackgroundColor: 'rgba(141,191,66, 1)',
      backgroundColor: 'rgba(141,191,66, 0.3)',
      borderColor: 'rgba(141,191,66, 1)'
    };
    this.recoveredLineChartData = [recoverdLineChartOptions];
  }

  configDeceasedLineChart(data): void {
    const deceasedLineChartOptions = {
      data,
      pointBorderWidth: 0.5,
      pointBorderColor: 'rgba(226,160,63, 0.9)',
      pointHoverBackgroundColor: 'rgba(226,160,63, 1)',
      pointHoverBorderColor: 'rgba(226,160,63, 1)',
      pointBackgroundColor: 'rgba(226,160,63, 1)',
      backgroundColor: 'rgba(226,160,63, 0.3)',
      borderColor: 'rgba(226,160,63, 1)'
    };
    this.deceasedLineChartData = [deceasedLineChartOptions];
  }

  configTestedLineChart(data): void {
    const testedLineChartOptions = {
      data,
      pointBorderWidth: 0.5,
      pointBorderColor: 'rgba(59,63,92, 0.9)',
      pointHoverBackgroundColor: 'rgba(59,63,92, 1)',
      pointHoverBorderColor: 'rgba(59,63,92, 1)',
      pointBackgroundColor: 'rgba(59,63,92, 1)',
      backgroundColor: 'rgba(59,63,92, 0.3)',
      borderColor: 'rgba(59,63,92, 1)'
    };
    this.testedLineChartData = [testedLineChartOptions];
  }

  configCriticalLineChart(data): void {
    const criticalLineChartOptions = {
      data,
      pointBorderWidth: 0.5,
      pointBorderColor: 'rgb(92,26,195, 0.9)',
      pointHoverBackgroundColor: 'rgba(92,26,195, 1)',
      pointHoverBorderColor: 'rgba(92,26,195, 1)',
      pointBackgroundColor: 'rgba(92,26,195, 1)',
      backgroundColor: 'rgba(92,26,195, 0.3)',
      borderColor: 'rgba(92,26,195, 1)'
    };
    this.criticalLineChartData = [criticalLineChartOptions];
  }



}
