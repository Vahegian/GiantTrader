import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AI {
  private httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json',
                                'Accept': 'text/plain'})
  };  

  private urls = {
    server : "http://172.20.0.4:5000",
    // server : "/ai",
    dnn_batch_pred_url : "/getnnbatchpred",
    get_models_url: "/getmodels"
  }
  
  constructor(private http: HttpClient) {}

  get_batch_pred(model_name, data): Observable<any>{
    data = JSON.stringify({"data":data, "model":model_name});
    return this.http.post<any>(this.urls.server+this.urls.dnn_batch_pred_url, 
            data, this.httpOptions);
  }

  get_models(): Observable<any>{
    return this.http.get<any>(this.urls.server+this.urls.get_models_url, this.httpOptions);
  }

}
