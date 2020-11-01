import { Component, OnInit } from '@angular/core';
import { Total } from '../models/total';
import { CovidDataService } from '../services/covid-data.service';

@Component({
  selector: 'app-current-stats',
  templateUrl: './current-stats.component.html',
  styleUrls: ['./current-stats.component.scss']
})
export class CurrentStatsComponent implements OnInit {
  total: Total = null;
  newCases = 0;
  activeChange = 0;
  newRecoveries = 0;
  newDeaths = 0;
  changesOptions = {
    duration: 1
  };

  constructor(private covidDataService: CovidDataService) { }

  ngOnInit(): void {
    this.getTotal();
  }

  // TODO: Update changes
  getTotal(): void {
    this.covidDataService.getTotal().subscribe((total: Total) => {
      this.total = total[0];

      const latest = this.total.cumulative[this.total.cumulative.length - 1];
      const secondLatest = this.total.cumulative[this.total.cumulative.length - 2];

      this.newCases = latest['Confirmed'] - secondLatest['Confirmed'];
      this.newRecoveries = latest['Recoveries'] - secondLatest['Recoveries'];
      this.newDeaths = latest['Mortalities'] - secondLatest['Mortalities'];
      this.activeChange = latest['Active'] - secondLatest['Active'];
    });
  }

}
