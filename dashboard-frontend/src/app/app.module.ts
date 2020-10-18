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

@NgModule({
  declarations: [
    AppComponent,
    CurrentStatsComponent,
    RegionsTableComponent,
    ChartsComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    HttpClientModule,
    FormsModule,
    CountUpModule,
    NgSelect2Module
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
