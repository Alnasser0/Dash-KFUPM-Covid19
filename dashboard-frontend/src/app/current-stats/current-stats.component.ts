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

  constructor(private covidDataService: CovidDataService) { }

  ngOnInit(): void {
    this.getTotal();
  }

  // TODO: Update changes
  getTotal(): void {
    this.covidDataService.getTotal().subscribe(total => {
      this.total = total[0];
      // const latest = this.total.daily[this.total.daily.length - 1];
      // this.newCases = latest['New Cases'];

    });
  }

}
