import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RollingDayBot {
  private httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json',
                                'Accept': 'text/plain'})
  };  

  private urls = {
    // server : "http://172.20.0.6:5000",
    server : "/bot",
    get_available_bots_url : "/getavalbots",
    get_running_bots_url : "/getrunningbots",
    start__stop_bot_url : "/start_stop_log_bot"
  }
  
  constructor(private http: HttpClient) {}

  get_bots(): Observable<any>{
    return this.http.get<any>(this.urls.server+this.urls.get_available_bots_url, 
                              this.httpOptions);
  }

  get_running_bots(): Observable<any>{
    return this.http.get<any>(this.urls.server+this.urls.get_running_bots_url, 
                              this.httpOptions);
  }

  startBot(bot, pair, uname): Observable<any>{
    var data = JSON.stringify({"pair":pair,"bot":bot, "action":"start", "uname":uname})
    return this.http.post<any>(this.urls.server+this.urls.start__stop_bot_url, data,
                                this.httpOptions)
  }

  stopBot(bot_id): Observable<any>{
    var data = JSON.stringify({"id":bot_id, "action":"stop"})
    return this.http.post<any>(this.urls.server+this.urls.start__stop_bot_url, data,
                                this.httpOptions)
  }

  BotLog(bot_id): Observable<any>{
    var data = JSON.stringify({"id":bot_id, "action":"log"})
    return this.http.post<any>(this.urls.server+this.urls.start__stop_bot_url, data,
                                this.httpOptions)
  }
}
