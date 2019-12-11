import { Component, OnInit } from '@angular/core';
import { EngineApiService } from 'src/app/services/engine/engine-api.service';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, Label } from 'ng2-charts';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnInit {
  public cb_open = false;
  public cb_high = false;
  public cb_low = false;
  public cb_close = false;
  public lineChartData = [
    { data: [], label: 'Open', backgroundColor: "rgba(255, 0, 0, 0.2)"},
    { data: [], label: 'High', backgroundColor: "rgba(0, 255, 0, 0.2)"},
    { data: [], label: 'Low', backgroundColor: "rgba(0, 0, 255, 0.2)"},
    { data: [], label: 'Close', backgroundColor: "rgba(0, 0, 0, 0.8)"}
  ];

  public lineChartLabels: Label[] = [];
  public lineChartOptions = {
    responsive: true,
  };
  public lineChartColors: Color[] = [
    // {
    //   backgroundColor: 'rgba(255,255,0,0.28)'
    // },
  ];
  public lineChartLegend = true;
  public lineChartPlugins = [];
  public lineChartType = 'line';
  public days = 7;

  constructor(public engine_api: EngineApiService){}

  ngOnInit() {
  }

  plot_chart(){
    this.engine_api.get_ohlc(this.engine_api.working_pair, this.days)
    .subscribe(data=>{
      this.lineChartData[0].data = [];
      this.lineChartData[1].data = [];
      this.lineChartData[2].data = [];
      this.lineChartData[3].data = [];
      this.lineChartLabels = [];
      for (var item in data){
        if (this.cb_open){
        this.lineChartData[0].data.push(data[item].open);}
        if (this.cb_high){
        this.lineChartData[1].data.push(data[item].high);}
        if (this.cb_low){
        this.lineChartData[2].data.push(data[item].low);}
        if (this.cb_close){
        this.lineChartData[3].data.push(data[item].close);}
        this.lineChartLabels.push(item);
      }
    });
  }

}
