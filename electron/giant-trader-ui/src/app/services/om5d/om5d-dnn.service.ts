import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Om5dDnnService {
  private httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json',
                                'Accept': 'text/plain'})
  };  

  private urls = {
    server : "http://0.0.0.0:10002",
    dnn_batch_pred_url : "/getnnbatchpred"
  }
  
  constructor(private http: HttpClient) {}

  get_batch_pred(data): Observable<any>{
    data = JSON.stringify({"data":data});
    return this.http.post<any>(this.urls.server+this.urls.dnn_batch_pred_url, 
            data, this.httpOptions);
  }

}
