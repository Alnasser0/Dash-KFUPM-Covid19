import { Component, OnInit } from '@angular/core';
import { Total } from 'src/app/models/total';
import { CovidDataService } from 'src/app/services/covid-data.service';

@Component({
  selector: 'app-current-stats',
  templateUrl: './current-stats.component.html',
  styleUrls: ['./current-stats.component.scss']
})
export class CurrentStatsComponent implements OnInit {
  total: Total = null;
  changesOptions = {
    duration: 1
  };

  constructor(private covidDataService: CovidDataService) { }

  ngOnInit(): void {
    this.getTotal();
  }

  getTotal(): void {
    this.covidDataService.total.subscribe(total => {
      if (total) {
        this.total = total;
      }
    });
  }

}
