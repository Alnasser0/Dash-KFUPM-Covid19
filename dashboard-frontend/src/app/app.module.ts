import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';

import { CountUpModule } from 'ngx-countup';
import { NgSelect2Module } from 'ng-select2';
import { ChartsModule } from 'ng2-charts';
import { SimulationComponent } from './simulation/simulation.component';
import { StatisticsComponent } from './statistics/statistics.component';
import { ChartsComponent } from './statistics/charts/charts.component';
import { CurrentStatsComponent } from './statistics/current-stats/current-stats.component';
import { MapComponent } from './statistics/map/map.component';
import { RegionsTableComponent } from './statistics/regions-table/regions-table.component';

const routes = [
  { path: '', component: StatisticsComponent },
  { path: 'simulation', component: SimulationComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    CurrentStatsComponent,
    RegionsTableComponent,
    ChartsComponent,
    MapComponent,
    SimulationComponent,
    StatisticsComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    RouterModule.forRoot(routes),
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
