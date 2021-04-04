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
  public show_reg = false;
  constructor(private engine_api: BinanceApiService, private router: Router) { }

  ngOnInit() {
  }

  login_user(uname, pass) {
    if (uname==="" && pass ==="") return 
    this.show_loggingin = true;
    this.engine_api.login_user(uname, pass)
      .subscribe((data) => {
        if (data.status == 1) {
          // this.engine_api.logged_in_user = data.uname;
          this.router.navigateByUrl('/main')
          // console.log(data)
        } else {
          this.show_loggingin = false;
          alert("Login Failed: Api key and secret not found");
          console.log(data);
        }
      });
    // console.log(uname +" : "+ pass)
  }

  reg_user(uname, pass, key, secret) {
    console.log(uname, pass, key, secret)
    if (uname==="" && pass ==="") return 
    this.show_reg = true;
    this.engine_api.create_user(uname, pass, key, secret)
      .subscribe((data) => {
        if (data.status == 1) {
          // this.engine_api.logged_in_user = data.uname;
          // this.router.navigateByUrl('/main')
          alert("Try logging in with the new account")
          this.show_reg = false;
          // console.log(data)
        } else {
          this.show_reg = false;
          alert("Registration failed");
          console.log(data);
        }
      });
    // console.log(uname +" : "+ pass)
  }

}
