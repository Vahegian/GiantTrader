import { Component, OnInit } from '@angular/core';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';

@Component({
  selector: 'app-open-orders',
  templateUrl: './open-orders.component.html',
  styleUrls: ['./open-orders.component.css']
})
export class OpenOrdersComponent implements OnInit {
  public open_order_rows = [];
  public update_progress = 0;
  constructor(private engine_api: BinanceApiService) { }

  ngOnInit() {
    this.update_open_orders()
    setInterval(() => {

      if (this.update_progress == 100) {
        this.update_open_orders()
        this.update_progress = 0
      }
      this.update_progress += 1
      // console.log(this.update_progress)

    }, 3000)
  }

  update_open_orders(){
    this.update_progress = 0
    this.open_order_rows = []
    this.engine_api.get_open_orders()
    .subscribe(data=>{
      // console.log(data);
      for (var i in data){
        this.open_order_rows.push([data[i]["orderId"], data[i]["symbol"],
                                   data[i]["side"], data[i]["type"], 
                                   parseFloat(data[i]["price"]).toFixed(4),
                                   parseFloat(data[i]["origQty"]).toFixed(4),
                                   parseFloat(data[i]["executedQty"]).toFixed(4), 
                                   parseFloat(data[i]["stopPrice"]).toFixed(4),
                                   data[i]["fee"]])
      }
    });
  }

  remove_order(id,pair,price,amount,fee){
    this.engine_api.cancel_order(id,pair,price,amount,fee)
    .subscribe(data=>{
      if (data.status==1){
        this.update_open_orders();
      }
    });
  }

}
