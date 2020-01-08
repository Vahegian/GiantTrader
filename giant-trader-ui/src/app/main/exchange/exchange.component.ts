import { Component, OnInit } from '@angular/core';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';

@Component({
  selector: 'app-exchange',
  templateUrl: './exchange.component.html',
  styleUrls: ['./exchange.component.css']
})
export class ExchangeComponent implements OnInit {
  // public pairs = [];
  // public selected_pair = "";
  constructor(public engine_api: BinanceApiService) { }

  ngOnInit() {
    // this.engine_api.get_lastPries()
    // .subscribe((data)=>{
    //   this.pairs = Object.keys(data);
    //   this.pairs.sort()
    //   if (this.pairs.length == 0){
    //     this.ngOnInit()
    //   }
    //   // console.log(this.pairs)
    // });
    // this.engine_api.working_pair = this.selected_pair;
    // console.log(this.engine_api.working_pair);
  }
}
