import { Component, OnInit } from '@angular/core';
import { Color, Label } from 'ng2-charts';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';

@Component({
  selector: 'app-chart-live',
  templateUrl: './chart-live.component.html',
  styleUrls: ['./chart-live.component.css']
})
export class ChartLiveComponent implements OnInit {
  public mainChartData = [
    { data: [], label: "please select a pair", backgroundColor: "rgba(50, 200, 120, 0.2)" }
  ];
  public mainChartLabels: Label[] = [];
  public mainChartOptions = {
    responsive: true,
  };
  public mainChartColors: Color[] = [];
  public mainChartLegend = true;
  public mainChartPlugins = [];
  public mainChartType = 'line';
  private temp_pair = "";
  public max_allowed_points = 60;
  public interval = 2;
  // public max_posible = 0;
  constructor(public binance_api: BinanceApiService) { }

  ngOnInit() {
    var timer_counter = 0;
    setInterval(() => {
      timer_counter++;
      if (timer_counter % this.interval == 0) {
        if (this.binance_api.working_pair != null) {
          this.show()
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
            for(let i=0; i<diff; i++){this.mainChartData[0].data.shift(); this.mainChartLabels.shift()}
          }
          // try {
          var date = new Date()
          this.mainChartData[0].data.push(parseFloat(data[this.temp_pair]).toFixed(6));
          this.mainChartLabels.push(date.toString().split(" ")[4]);
          // } catch{ }
        });
    } else {
      if (this.binance_api.working_pair != null) {
        this.temp_pair = this.binance_api.working_pair;
        this.mainChartData[0].label = this.temp_pair;
        this.mainChartLabels = [];
        this.mainChartData[0].data = [];
      }
    }
  }

}
