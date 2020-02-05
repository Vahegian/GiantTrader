import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

interface Login_resp{
  message:string,
  status:number,
  uname:string}

@Injectable({
  providedIn: 'root'
})
export class BinanceApiService {
  public logged_in_user = null;
  public working_pair = null;
  private httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json'})
  };  

  private urls = {
    // server : "http://172.20.0.3:5000",
    server:"/binance",
    u_login_url : "/inuser",
    u_logout_url: "/outuser",
    u_get_wallet_url : "/ud/wallet",
    u_get_open_orders_url : "/ud/oorders",
    u_get_last_prices_url : "/lastprices",
    u_cancel_open_order_url : "/ocancel",
    u_sell_limit_url : "/lsell",
    u_buy_limit_url : "/lbuy",
    u_sell_market_url : "/msell",
    u_buy_market_url : "/mbuy",
    u_get_pair_fee_url : "/pairfee",
    u_get_ohlc_url : "/ohlcv",
    u_strategies_url : "/strategies"
  }
  
  constructor(private http: HttpClient) {
    // console.log(window.location.hostname);
  }

  login_user(uname, pass): Observable<Login_resp>{
    return this.http.post<Login_resp>(this.urls.server+this.urls.u_login_url, JSON.stringify({"uname":uname, "upass":pass}), this.httpOptions);
  }

  logout_user(uname): Observable<Login_resp>{
    return this.http.post<Login_resp>(this.urls.server+this.urls.u_logout_url, 
            JSON.stringify({"uname":uname}), this.httpOptions);
  }

  get_login_users(): Observable<any>{
    return this.http.get<any>(this.urls.server+this.urls.u_login_url, this.httpOptions);
  }

  get_lastPries(): Observable<any> {
    return this.http.post<any>(this.urls.server+this.urls.u_get_last_prices_url, JSON.stringify({"uname":this.logged_in_user}), this.httpOptions);
  }

  get_pair_fee(pair): Observable<any>{
    return this.http.post<any>(this.urls.server+this.urls.u_get_pair_fee_url, 
      JSON.stringify({"uname":this.logged_in_user,
                      "pair":pair}), this.httpOptions);
  }

  place_buy_order(pair, price, amount, fee): Observable<any>{
    // console.log(fee)
    return this.http.post<any>(this.urls.server+this.urls.u_buy_limit_url, 
      JSON.stringify({"uname":this.logged_in_user,
                      "pair":pair,
                      "price":price,
                      "amount":amount,
                      "fee":fee}), this.httpOptions);
  }

  place_market_buy_order(pair, amount, fee): Observable<any>{
    // console.log(fee)
    return this.http.post<any>(this.urls.server+this.urls.u_buy_market_url, 
      JSON.stringify({"uname":this.logged_in_user,
                      "pair":pair,
                      "amount":amount,
                      "fee":fee}), this.httpOptions);
  }

  place_sell_order(pair, price, amount, fee): Observable<any>{
    // console.log(fee)
    return this.http.post<any>(this.urls.server+this.urls.u_sell_limit_url, 
      JSON.stringify({"uname":this.logged_in_user,
                      "pair":pair,
                      "price":price,
                      "amount":amount,
                      "fee":fee}), this.httpOptions);
  }

  place_market_sell_order(pair, amount, fee): Observable<any>{
    // console.log(fee)
    return this.http.post<any>(this.urls.server+this.urls.u_sell_market_url, 
      JSON.stringify({"uname":this.logged_in_user,
                      "pair":pair,
                      "amount":amount,
                      "fee":fee}), this.httpOptions);
  }

  get_open_orders(): Observable<any> {
    return this.http.post<any>(this.urls.server+this.urls.u_get_open_orders_url,
       JSON.stringify({"uname":this.logged_in_user}), this.httpOptions);
  }

  cancel_order(orderId, pair, price, amount, fee): Observable<any>{
    return this.http.post<any>(this.urls.server+this.urls.u_cancel_open_order_url, 
      JSON.stringify({"uname":this.logged_in_user,
                      "orderId":orderId,
                      "pair":pair,
                      "price":price,
                      "amount":amount,
                      "fee":fee}), this.httpOptions);
  }

  get_wallet(): Observable<any> {
    return this.http.post<any>(this.urls.server+this.urls.u_get_wallet_url,
       JSON.stringify({"uname":this.logged_in_user}), this.httpOptions);
  }

  get_ohlc(pair, days): Observable<any>{
    // console.log(fee)
    return this.http.post<any>(this.urls.server+this.urls.u_get_ohlc_url, 
      JSON.stringify({"uname":this.logged_in_user,
                      "pair":pair,
                      "days":days,}), this.httpOptions);
  }

}
