import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';


import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { CurrentStatsComponent } from './current-stats/current-stats.component';
import { RegionsTableComponent } from './regions-table/regions-table.component';
import { ChartsComponent } from './charts/charts.component';

import { CountUpModule } from 'ngx-countup';
import { NgSelect2Module } from 'ng-select2';
import { ChartsModule } from 'ng2-charts';
import { MapComponent } from './map/map.component';

@NgModule({
  declarations: [
    AppComponent,
    CurrentStatsComponent,
    RegionsTableComponent,
    ChartsComponent,
    MapComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    HttpClientModule,
    FormsModule,
    CountUpModule,
    NgSelect2Module,
    ChartsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
