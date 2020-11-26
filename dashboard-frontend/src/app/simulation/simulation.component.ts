import { Component, OnInit } from '@angular/core';
import { CovidDataService } from '../services/covid-data.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-simulation',
  templateUrl: './simulation.component.html',
  styleUrls: ['./simulation.component.scss']
})
export class SimulationComponent implements OnInit {
  framerate = 5;
  finalStep = 1000;
  src: any;

  constructor(private covidDataService: CovidDataService, private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
  }

  onSubmit(): void {
    this.src = null;
    this.covidDataService.simulate({ framerate: this.framerate, finalStep: this.finalStep })
      .subscribe(response => {
        console.log(response);
        this.src = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(response));
        console.log(this.src);
      });
  }

}
