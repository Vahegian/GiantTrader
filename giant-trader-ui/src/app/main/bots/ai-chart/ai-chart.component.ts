import { Component, OnInit, Input, EventEmitter } from '@angular/core';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';
import { Color, Label } from 'ng2-charts';
import { AI } from 'src/app/services/ai/ai.service';

@Component({
  selector: 'app-ai-chart',
  templateUrl: './ai-chart.component.html',
  styleUrls: ['./ai-chart.component.css']
})
export class AIChartComponent implements OnInit {
  public days = 60;
  @Input() public model_name;
  public ai_preds = null;
  public lineChartData = [
    { data: [], label: 'Close', backgroundColor: "rgba(100, 48, 240, 0.3)",
                borderColor: '', type: 'line'},
    { data: [], label: '', backgroundColor:[], type: 'bar'},
   ];

  public lineChartLabels: Label[] = [];
  public lineChartOptions = {
    responsive: true,
  };
  public lineChartColors: Color[] = [];
  public lineChartLegend = true;
  public lineChartPlugins = [];
  public lineChartType = 'bar';

  constructor(public engine_api: BinanceApiService, public ai: AI) {}

  ngOnInit() {
  }
// hcol
  plot_chart(){
    this.engine_api.get_ohlc(this.engine_api.working_pair, this.days)
    .subscribe(data=>{
      this.lineChartData[0].data = [];
      this.lineChartData[1].data = [];
      this.lineChartData[1].backgroundColor = [];
      this.lineChartLabels = [];
      var final_data = []
      var temp = [[],[],[],[]];
      for (var item in data){
        var close = data[item].close;
        this.lineChartData[0].data.push(close);
        this.lineChartLabels.push(item);
        temp[0].push(data[item].high)
        temp[1].push(close)
        temp[2].push(data[item].open)
        temp[3].push(data[item].low)
        if (temp[0].length==30){
          var batch = [];
          for (var index in temp){
            batch = batch.concat(temp[index]);
            temp[index].shift()
          }
          final_data.push(JSON.stringify(batch));
        }
      }
      this.add_predictions(final_data);
    });
  }

  add_predictions(final_data){
    // console.log(this.model_name)
    this.ai.get_batch_pred(this.model_name,JSON.stringify(final_data))
      .subscribe(preds=>{
        // console.log(preds);
        this.ai_preds = preds["preds"];
        var diff = this.lineChartData[0]["data"].length-this.ai_preds.length;
        this.lineChartData[1].data = new Array(diff).fill(0);
        this.lineChartData[1].backgroundColor = new Array(diff).fill("rgba(0, 0, 0, 0.0)");
        for (var pred in this.ai_preds){
          pred = this.ai_preds[pred]
          // console.log(pred);
          // var conf = parseFloat(pred["conf"]);
          var price = parseFloat(this.lineChartData[0]["data"][diff]);
          var bar_height = price
          // console.log(diff+":"+conf+":"+price+":"+bar_height);
          if (pred["side"] == "BUY"){
            this.lineChartData[1].data.push(bar_height);
            this.lineChartData[1].backgroundColor.push("rgba(0, 255, 0, 0.7)");
          }else{
            this.lineChartData[1].data.push(bar_height);
            this.lineChartData[1].backgroundColor.push("rgba(255, 0, 0, 0.7)");
          }
          diff++;
        }
        // console.log(diff);
        // console.log(this.lineChartData)
      });
  }

}
