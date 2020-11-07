import { Component, Input, OnChanges, OnInit, SimpleChanges, ViewChild } from '@angular/core';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Label } from 'ng2-charts';
import { Region } from '../models/region';
import { Total } from '../models/total';
import { CovidDataService } from '../services/covid-data.service';


const TICKS_COLOR = '#FFFFFF';
const CONFIRMED_COLOR = '#2196F3';
const ACTIVE_COLOR = '#E7515A';
const RECOVERED_COLOR = '#8DBF42';
const DECEASED_COLOR = '#E2A03F';
const TESTED_COLOR = '#3B3F5C';
const CRITICAL_COLOR = '#5C1AC3';

@Component({
  selector: 'app-charts',
  templateUrl: './charts.component.html',
  styleUrls: ['./charts.component.scss']
})
export class ChartsComponent implements OnInit, OnChanges {

  // @Input() selectedRegion: Region;

  regions: Region[];
  total: Total;

  regionNames: string[];
  defaultRegion = 'Saudi Arabia';
  selectedRegion = this.defaultRegion;

  displayMode = 'cumulative';

  public lineChartType = 'line';
  public barChartType = 'bar';

  public confirmedLineChartData: ChartDataSets[];
  public activeLineChartData: ChartDataSets[];
  public recoveredLineChartData: ChartDataSets[];
  public deceasedLineChartData: ChartDataSets[];
  public testedLineChartData: ChartDataSets[];
  public criticalLineChartData: ChartDataSets[];

  public confirmedBarChartData: ChartDataSets[];
  public activeBarChartData: ChartDataSets[];
  public recoveredBarChartData: ChartDataSets[];
  public deceasedBarChartData: ChartDataSets[];
  public testedBarChartData: ChartDataSets[];


  public cumulativeLabels: Label[];
  public dailyLabels: Label[];

  public chartOptions: ChartOptions = {
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
      intersect: false,
      backgroundColor: '#000',
      titleAlign: 'center',
      titleMarginBottom: 10,
      titleFontSize: 16,
      displayColors: false,
      xPadding: 10,
      yPadding: 10,
      bodySpacing: 10,
      bodyFontSize: 15,
      callbacks: {
        label: (tooltipItem, data) => {
          return (+tooltipItem.value).toLocaleString();
        }
      }
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
          fontColor: TICKS_COLOR + 'CC',
          maxTicksLimit: 10
        },
        gridLines: {
          drawOnChartArea: false,
          lineWidth: 1,
          color: TICKS_COLOR + 'CC'
        }
      }],
      yAxes: [{
        ticks: {
          fontSize: 13,
          fontColor: TICKS_COLOR + 'CC',
          callback: (value) => value.toLocaleString(),
          maxTicksLimit: 10
        },
        gridLines: {
          drawOnChartArea: false,
          lineWidth: 0.9,
          color: TICKS_COLOR + 'CC'
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

    switch (mode) {
      case 'daily':
        this.updateCharts();
        this.chartOptions.scales.yAxes[0].type = 'linear';
        break;

      case 'cumulative':
        this.chartOptions.scales.yAxes[0].type = 'linear';
        break;

      case 'log':
        this.chartOptions.scales.yAxes[0].type = 'logarithmic';
        break;
    }
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

      if (this.displayMode === 'daily') {
        const dailyTested = newRegion.daily.map(c => c['Tested']);
        this.testedBarChartData = this.configBarChart(dailyTested, TESTED_COLOR);

      } else {
        const cumulativeTested = newRegion.cumulative.map(c => c['Tested']);
        this.testedLineChartData = this.configLineChart(cumulativeTested, TESTED_COLOR);

        const cumulativeCritical = newRegion.cumulative.map(c => c['Critical']);
        this.criticalLineChartData = this.configLineChart(cumulativeCritical, CRITICAL_COLOR);
      }
    } else {
      newRegion = this.regions.find(region => region.name === this.selectedRegion);
    }

    if (this.displayMode === 'daily') {
      const dailyConfirmed = newRegion.daily.map(c => c['New Cases']);
      this.confirmedBarChartData = this.configBarChart(dailyConfirmed, CONFIRMED_COLOR);

      const dailyActive = newRegion.daily.map(c => c['New Cases']);
      this.activeBarChartData = this.configBarChart(dailyActive, ACTIVE_COLOR);

      const dailyRecovered = newRegion.daily.map(c => c['Recoveries']);
      this.recoveredBarChartData = this.configBarChart(dailyRecovered, RECOVERED_COLOR);

      const dailyDeceased = newRegion.daily.map(c => c['Mortalities']);
      this.deceasedBarChartData = this.configBarChart(dailyDeceased, DECEASED_COLOR);

      this.dailyLabels = newRegion.daily.map(d => d['Date']);

    } else {
      const cumulativeConfirmed = newRegion.cumulative.map(c => c['Confirmed']);
      this.confirmedLineChartData = this.configLineChart(cumulativeConfirmed, CONFIRMED_COLOR);

      const cumulativeActive = newRegion.cumulative.map(c => c['Active']);
      this.activeLineChartData = this.configLineChart(cumulativeActive, ACTIVE_COLOR);

      const cumulativeRecovered = newRegion.cumulative.map(c => c['Recoveries']);
      this.recoveredLineChartData = this.configLineChart(cumulativeRecovered, RECOVERED_COLOR);

      const cumulativeDeceased = newRegion.cumulative.map(c => c['Mortalities']);
      this.deceasedLineChartData = this.configLineChart(cumulativeDeceased, DECEASED_COLOR);

      this.cumulativeLabels = newRegion.cumulative.map(d => d['Date']);
    }

  }

  // Configures chart options for Line chart
  configLineChart(data, color): Array<any> {
    const options = {
      data,
      pointBorderWidth: 0.5,
      pointBorderColor: color + 'E6',
      pointHoverBackgroundColor: color + 'FF',
      pointHoverBorderColor: color + 'FF',
      pointBackgroundColor: color + 'FF',
      backgroundColor: color + '4D',
      borderColor: color + 'FF'
    };

    return [options];
  }

  configBarChart(data, color): Array<any> {
    const options = {
      data,
      borderWidth: 1,
      hoverBorderWidth: 5,
      hoverBackgroundColor: color + 'FF',
      hoverBorderColor: color + 'FF',
      backgroundColor: color + '33',
      borderColor: color + 'FF'
    };

    return [options];
  }
}
