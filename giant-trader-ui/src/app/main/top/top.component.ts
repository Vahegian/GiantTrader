import { Component, OnInit } from '@angular/core';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-top',
  templateUrl: './top.component.html',
  styleUrls: ['./top.component.css']
})
export class TopComponent implements OnInit {
  public show_logout = true;
  public show_loading = true;
  public pairs = [];
  public in_user = "";
  private pair_prices_to_show = [["BTCUSDT",0.0, ""], ["BCHUSDT",0.0,""], ["ETHUSDT",0.0, ""], ["XRPUSDT",0.0,""], ["LTCUSDT",0.0,""], ["EOSUSDT",0.0,""],["BATUSDT",0.0,""]]
  public live_users = []
  constructor(public engine_api: BinanceApiService, private router: Router) {
    this.in_user = engine_api.logged_in_user;
  }

  ngOnInit() {
    setInterval(() => {
      this.engine_api.get_lastPries()
        .subscribe((data) => {
        for (var i in this.pair_prices_to_show){
          var new_price = parseFloat(data[this.pair_prices_to_show[i][0]]).toFixed(4);
          if (new_price>this.pair_prices_to_show[i][1]){
            this.pair_prices_to_show[i][2] = "text-success"
          }else{
            this.pair_prices_to_show[i][2] = "text-danger"
          }
          this.pair_prices_to_show[i][1] = new_price;
        }
        });
      this.get_live_users();
    }, 5000);
    this.populate_pair_selector();
  }

  populate_pair_selector(){
    this.engine_api.get_lastPries()
    .subscribe((data)=>{
      this.pairs = Object.keys(data);
      this.pairs.sort()
      if (this.pairs.length == 0){
        this.populate_pair_selector();
      }
      // console.log(this.pairs)
    });
  }

  get_live_users(){
    this.engine_api.get_login_users()
    .subscribe(data=>{
      // console.log(data);
      this.live_users = data.users;
      this.show_loading = false;
    });
  }

  logout(){
    this.engine_api.logout_user(this.engine_api.logged_in_user)
    .subscribe(data=>{
      if (data.status == 1){
        this.router.navigateByUrl("/login")
        location.reload()
      }
    });
  }
}
