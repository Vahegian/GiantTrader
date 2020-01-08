import { Component, OnInit } from '@angular/core';
import { BinanceApiService } from '../services/binance/binance-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  constructor(private engine_api: BinanceApiService, private router: Router) { }

  ngOnInit() {
  }

  login_user(uname, pass){
    this.engine_api.login_user(uname, pass)
    .subscribe((data)=>{
      if (data.status == 1){
        this.engine_api.logged_in_user = data.uname;
        this.router.navigateByUrl('/main') 
        // console.log(data)
      }
    });
    // console.log(uname +" : "+ pass)
  }

}
