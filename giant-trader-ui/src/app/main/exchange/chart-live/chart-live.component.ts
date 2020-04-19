import { Component, OnInit } from '@angular/core';
import { Color, Label } from 'ng2-charts';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';

@Component({
  selector: 'app-chart-live',
  templateUrl: './chart-live.component.html',
  styleUrls: ['./chart-live.component.css']
})
export class ChartLiveComponent implements OnInit {
  public showLiveChart = false;

  public mainChartData = [
    { data: [], label: "please select a pair", backgroundColor: [] }
  ];
  public mainChartLabels: Label[] = [];
  public mainChartOptions = {
    responsive: true,
  };
  public mainChartColors: Color[] = [];
  public mainChartLegend = true;
  public mainChartPlugins = [];
  public mainChartType = 'bar';
  private temp_pair = "";
  public max_allowed_points = 60;
  public interval = 2;
  // public max_posible = 0;
  constructor(public binance_api: BinanceApiService) { }

  private prev_price = -0.1;

  ngOnInit() {
    var timer_counter = 0;
    setInterval(() => {
      timer_counter++;
      if (timer_counter % this.interval == 0) {
        if (this.binance_api.working_pair != null) {
          if (this.showLiveChart) {
            this.show();
          }
        }
        timer_counter = 0;
      }
    }, 2000);
  }

  show() {
    if (this.temp_pair.length > 0 && this.temp_pair == this.binance_api.working_pair) {
      this.binance_api.get_lastPries()
        .subscribe(data => {
          // console.log(data);
          if (this.mainChartData[0].data.length > this.max_allowed_points) {
            var diff = this.mainChartData[0].data.length - this.max_allowed_points
            for (let i = 0; i < diff; i++) { this.mainChartData[0].data.shift(); this.mainChartLabels.shift(); this.mainChartData[0].backgroundColor.shift() }
          }
          // try {
          // if (this.prev_price == null) { this.prev_price = parseFloat(data[this.temp_pair]); }
          var date = new Date()
          let prcent_diff = 100 - ((((parseFloat(data[this.temp_pair]) / this.prev_price))) * 100);
          this.mainChartData[0].data.push(Math.abs(prcent_diff).toFixed(2));
          this.mainChartLabels.push(date.toString().split(" ")[4]);
          if (prcent_diff > 0.000000) {
            this.mainChartData[0].backgroundColor.push("rgba(50, 200, 120, 0.2)");
          } else {
            this.mainChartData[0].backgroundColor.push("rgba(200, 50, 50, 0.2)");
          }
          this.prev_price = parseFloat(data[this.temp_pair]);
          // } catch{ }
        });
    } else {
      if (this.binance_api.working_pair != null) {
        this.temp_pair = this.binance_api.working_pair;
        this.mainChartData[0].label = this.temp_pair;
        this.mainChartLabels = [];
        this.mainChartData[0].data = [];
        this.prev_price = 0.0
        this.mainChartData[0].backgroundColor = []
      }
    }
  }

}
