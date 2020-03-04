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
    { data: [], label: 'Price', borderColor: "rgba(66, 12, 89, 1.0)", backgroundColor:"rgba(255, 255, 255, 0.0)", type: 'line'},
    { data: [], label: 'Buy signal', fill: false, borderColor:"rgba(0, 255, 0, 0.3)", type: 'line'},
    { data: [], label: 'Hodl signal', fill: false, borderColor:"rgba(0, 0, 255, 0.3)", type: 'line'},
    { data: [], label: 'Sell signal', fill: false, borderColor:"rgba(255, 0, 0, 0.3)", type: 'line'},
    { data: [], label: 'Performance', fill: false, borderColor:"rgba(219, 199, 132, 0.9)", type: 'line'}
   ];

  public lineChartLabels: Label[] = [];
  public lineChartOptions = {
    responsive: true,
  };
  public lineChartColors: Color[] = [];
  public lineChartLegend = true;
  public lineChartPlugins = [];
  public lineChartType = 'line';

  constructor(public engine_api: BinanceApiService, public ai: AI) {}

  ngOnInit() {
  }
// hcol
  plot_chart(){
    this.engine_api.get_ohlc(this.engine_api.working_pair, this.days)
    .subscribe(data=>{
      for (let item of this.lineChartData){
        item.data = []
      }
      this.lineChartLabels = [];
      let final_data = []
      for (let item in data){
        let close = data[item].close;
        this.lineChartData[0].data.push(parseFloat(close));
        this.lineChartLabels.push(item);
        final_data.push(data[item])
      }
      this.add_predictions(final_data);
    });
  }

  add_predictions(final_data){
    let qty = 0.0
    let preds_started = false;
    alert("Loading '"+this.model_name+"'  please wait ....")
    this.ai.get_batch_pred(this.model_name,JSON.stringify(final_data))
      .subscribe(data=>{
          let preds = data.preds
          let max_price = Math.max(...this.lineChartData[0].data)*1.5;
          let buget = 0.0;
          for (let index in this.lineChartData[0].data){
            let buy =  parseFloat(preds[index][0]);
            let hodl = parseFloat(preds[index][1]);
            let sell = parseFloat(preds[index][2]);
            this.lineChartData[1].data.push(buy*max_price);
            this.lineChartData[2].data.push(hodl*max_price);
            this.lineChartData[3].data.push(sell*max_price);
            let curPrice = parseFloat(this.lineChartData[0].data[index]);
            
            if (buy!=0 && sell!=0 && hodl!=0 && !preds_started){buget = curPrice; preds_started=true}

            if (buy>sell && buy>hodl && buget>0.0){
              this.lineChartData[4].data.push(buget)
              qty = buget/curPrice;
            }else if (sell>buy && sell>hodl && qty>0){
              buget = curPrice*qty;
              this.lineChartData[4].data.push(buget)
            }else{
              this.lineChartData[4].data.push(buget)
            }
          }
      });
  }

}
