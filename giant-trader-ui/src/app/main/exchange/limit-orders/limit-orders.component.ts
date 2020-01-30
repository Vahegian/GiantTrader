import { Component, OnInit } from '@angular/core';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';

@Component({
  selector: 'app-limit-orders',
  templateUrl: './limit-orders.component.html',
  styleUrls: ['./limit-orders.component.css']
})
export class LimitOrdersComponent implements OnInit {
  public side = ["buy", "btn bg-white", "btn bg-success"];
  public isMarket = false;
  // public working_pair = "None"
  constructor(public engine_api: BinanceApiService) { }

  ngOnInit() {
    // this.working_pair=this.engine_api.working_pair;
  }

  select_side() {
    if (this.side[0] == "buy") {
      this.side = ["sell", "btn bg-danger", "btn bg-white"];
    } else {
      this.side = ["buy", "btn bg-white", "btn bg-success"];
    }
  }

  place_limit_order(price, amount) {
    if (price.length > 6 || amount.length > 6) {
      alert("numper of characters is more than 6!")
    } else {
      var pair = this.engine_api.working_pair;
      price = parseFloat(price);
      amount = parseFloat(amount);
      this.engine_api.get_pair_fee(pair)
        .subscribe((data) => {
          // console.log(data);
          var fee = parseFloat(data.taker) * 100;
          if (this.side[0] == "buy") {
            this.engine_api.place_buy_order(pair, price, amount, fee)
              .subscribe(ndata => {
                if (ndata.status == 1) {
                  alert("BUY, Success!")
                } else { alert(ndata.message) }
              });
          } else {
            this.engine_api.place_sell_order(pair, price, amount, fee)
              .subscribe(ndata => {
                if (ndata.status == 1) {
                  alert("SELL, Success!")
                } else { alert(ndata.message) }
              });
          }
        });
    }
    // console.log(price+" : "+amount)
  }

  place_market_order(amount) {
    if (amount.length > 6) {
      alert("numper of characters is more than 6!")
    } else {
      var pair = this.engine_api.working_pair;
      amount = parseFloat(amount);
      this.engine_api.get_pair_fee(pair)
        .subscribe((data) => {
          var fee = parseFloat(data.taker) * 100;
          if (this.side[0] == "buy") {
            this.engine_api.place_market_buy_order(pair, amount, fee)
              .subscribe(ndata => {
                if (ndata.status == 1) {
                  alert("BUY, Success!")
                } else { alert(ndata.message) }
              });
          } else {
            this.engine_api.place_market_sell_order(pair, amount, fee)
              .subscribe(ndata => {
                if (ndata.status == 1) {
                  alert("SELL, Success!")
                } else { alert(ndata.message) }
              });
          }
        });
    }
  }

}
