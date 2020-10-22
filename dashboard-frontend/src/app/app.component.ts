import { Component } from '@angular/core';
import { City } from './models/city';
import { Region } from './models/region';
import { Total } from './models/total';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  selectedCity: City;
  selectedRegion: Region;
  total: Total;
  showTotal: boolean;

  selectCity(city: City): void {
    this.selectedCity = city;
  }

  selectRegion(region: Region): void {
    this.selectedRegion = region;
  }

  selectTotal(total: Total): void {
    this.total = total;
  }

  showTotalFlag(flag: boolean): void {
    this.showTotal = flag;
  }

}
