import { Component, OnInit } from '@angular/core';
import { AI } from 'src/app/services/ai/ai.service';

@Component({
  selector: 'app-bots',
  templateUrl: './bots.component.html',
  styleUrls: ['./bots.component.css']
})
export class BotsComponent implements OnInit {
  public selected_model = "";
  public models = [];
  public show_ai = false;
  public show_bots = false;
  constructor(private ai_api: AI) { }

  ngOnInit() {
    this.ai_api.get_models()
    .subscribe(data=>{
      this.models = data.models;
    })
  }

  update_show_ai(){
    this.show_ai = !this.show_ai;
  }
  update_show_bots(){
    this.show_bots = !this.show_bots;
  }
}
