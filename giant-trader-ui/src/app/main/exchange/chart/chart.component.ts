import { Component, OnInit } from '@angular/core';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, Label } from 'ng2-charts';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnInit {
  public show_chart = false;
  public cb_open = false;
  public cb_high = false;
  public cb_low = false;
  public cb_close = false;
  public mainChartData = [
    { data: [], label: 'Open', backgroundColor: "rgba(255, 0, 0, 0.2)"},
    { data: [], label: 'High', backgroundColor: "rgba(0, 255, 0, 0.2)"},
    { data: [], label: 'Low', backgroundColor: "rgba(0, 0, 255, 0.2)"},
    { data: [], label: 'Close', backgroundColor: "rgba(0, 0, 0, 0.8)"}
  ];
  public weekChartData = [
    { data: [], label: 'per 7 days', backgroundColor: "rgba(0, 255, 0, 0.2)"}
  ];
  public weekChartLabels: Label[] = [];
  public monthChartData = [
    { data: [], label: 'per 30 days', backgroundColor: "rgba(0, 0, 255, 0.2)"}
  ];
  public monthChartLabels: Label[] = [];

  public mainChartLabels: Label[] = [];
  public mainChartOptions = {
    responsive: true,
  };
  public mainChartColors: Color[] = [];
  public mainChartLegend = true;
  public mainChartPlugins = [];
  public mainChartType = 'line';
  public days = 7;

  constructor(public engine_api: BinanceApiService){}

  ngOnInit() {
  }

  plot_chart(){
    this.engine_api.get_ohlc(this.engine_api.working_pair, this.days)
    .subscribe(data=>{
      this.mainChartData[0].data = [];
      this.mainChartData[1].data = [];
      this.mainChartData[2].data = [];
      this.mainChartData[3].data = [];
      this.mainChartLabels = [];
      for (var item in data){
        if (this.cb_open){
        this.mainChartData[0].data.push(data[item].open);}
        if (this.cb_high){
        this.mainChartData[1].data.push(data[item].high);}
        if (this.cb_low){
        this.mainChartData[2].data.push(data[item].low);}
        if (this.cb_close){
        this.mainChartData[3].data.push(data[item].close);}
        this.mainChartLabels.push(item);
      }
      this.plot_weekly(data);
      this.plot_monthly(data);
    });
  }

  get_chart_data_per_days(data, days){
    var chartdata = [];
    var labels = [];
    var count = 0;
    for(var item in data){
      if (count%days==0){
        chartdata.push(data[item].close);
        labels.push(item);
      }
      count++;
    }
    return [chartdata, labels]
  }

  plot_weekly(data){
    var chart_data = this.get_chart_data_per_days(data, 7);
    this.weekChartData[0].data = chart_data[0];
    this.weekChartLabels = chart_data[1];
  }

  plot_monthly(data){
    var chart_data = this.get_chart_data_per_days(data, 30);
    this.monthChartData[0].data = chart_data[0];
    this.monthChartLabels = chart_data[1];
  }
}
