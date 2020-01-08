import { Component, OnInit } from '@angular/core';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.css']
})
export class WalletComponent implements OnInit {
  public wallet_content = [];
  public wallet_total = 0.0;
  public update_progress = 0;
  constructor(private engine_api: BinanceApiService) { }

  ngOnInit() {
    this.update_wallet()
    setInterval(() => {

      if (this.update_progress == 100) {
        this.update_wallet()
        this.update_progress = 0
      }
      this.update_progress += 1
      // console.log(this.update_progress)

    }, 3000)
  }

  update_wallet() {
    this.update_progress = 0
    this.engine_api.get_wallet()
      .subscribe(data => {
        // console.log(data);
        this.engine_api.get_lastPries()
          .subscribe(lprices => {
            this.wallet_content = [];
            this.wallet_total = 0.0;
            for (var item in data) {
              var free = parseFloat(data[item].free)
              var locked = parseFloat(data[item].locked)
              var total = this.get_total_price_of_asset(item,
                free, locked, lprices);
              this.wallet_total += total;
              this.wallet_content.push([item, free.toFixed(4),
                locked.toFixed(4), total.toFixed(4)])
            }
          });
      });
  }

  get_total_price_of_asset(asset, free, locked, last_prices) {
    var total_of_asset = parseFloat(free) + parseFloat(locked);
    var pair_to_check_with = ["BTC", "ETH", "BNB", "XRP"]
    if (asset == "USDT" || asset == "USDC") {
      // total_money_in_wallet += total_of_asset;
      // console.log(asset+" : 1")
      return total_of_asset;
    }
    if (last_prices[asset + "USDT"]) {
      var total = total_of_asset * parseFloat(last_prices[asset + "USDT"]);
      // total_money_in_wallet += total;
      // console.log(asset+" : 2")
      return total;
    } else {
      for (var index in pair_to_check_with) {
        var asset_pair_price = last_prices[asset + pair_to_check_with[index]]
        if (asset_pair_price) {
          var pair_price = last_prices[pair_to_check_with[index] + "USDT"]
          var total = total_of_asset * (parseFloat(asset_pair_price) * parseFloat(pair_price))
          // total_money_in_wallet += total;
          // console.log(asset+" : 3")
          return total;
        }
      }
      // console.log(asset+" : 4")
      return 0.0
    }
  }

}
