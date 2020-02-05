import { Component, OnInit } from '@angular/core';
import { BinanceApiService } from '../services/binance/binance-api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  public show_loggingin = false;
  constructor(private engine_api: BinanceApiService, private router: Router) { }

  ngOnInit() {
  }

  login_user(uname, pass) {
    this.show_loggingin = true;
    this.engine_api.login_user(uname, pass)
      .subscribe((data) => {
        if (data.status == 1) {
          this.engine_api.logged_in_user = data.uname;
          this.router.navigateByUrl('/main')
          // console.log(data)
        } else {
          this.show_loggingin = false;
          alert("Login Failed");
          // this.router.navigateByUrl('/main')
        }
      });
    // console.log(uname +" : "+ pass)
  }

}
