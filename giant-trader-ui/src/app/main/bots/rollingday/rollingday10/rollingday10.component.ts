import { Component, OnInit } from '@angular/core';
import { RollingDayBot } from 'src/app/services/bots/bots.service';
import { BinanceApiService } from 'src/app/services/binance/binance-api.service';

@Component({
  selector: 'app-rollingday10',
  templateUrl: './rollingday10.component.html',
  styleUrls: ['./rollingday10.component.css']
})
export class Rollingday10Component implements OnInit {
  public running_bots = []
  public bots = []
  public bot_log = []
  public logging_bot_id = "\"press show log\""
  public show_removing = false;
  public modal_info_for_bot = []

  constructor(private rollingdaybot:RollingDayBot, private binance:BinanceApiService) { }

  ngOnInit() {
    this.rollingdaybot.get_bots()
    .subscribe(data=>{
      // console.log(data);
      for(var i in data){
        this.bots.push(data[i]);
      }
    })
    this.update();
    setInterval(()=>{this.update()}, 10000);
  }

  update(){
    this.rollingdaybot.get_running_bots()
    .subscribe(data=>{
      this.running_bots = data;
    })
  }

  remove_bot(id){
    alert("removing please wait might take a minute ...");
    this.show_removing = true;
    this.rollingdaybot.stopBot(id)
    .subscribe(data=>{
      if (data.status == 1){
        this.update();
        alert("removed "+id);
        this.show_removing = false;
      }
    })
  }

  show_bot_log(id){
    this.rollingdaybot.BotLog(id)
    .subscribe(data=>{
      if (data.status==1){
        this.logging_bot_id = id;
        this.bot_log = data.log;
      }else{
        alert("logging failed!")
      }
    })
  }

  add_bot(bot_name){
    // console.log(bot_name)
    this.rollingdaybot.startBot(bot_name, this.binance.working_pair, this.binance.logged_in_user)
    .subscribe(data=>{
      // console.log(data);
      if (data.status == 1){
        this.update()
      }
    })
  }

  show_more_info(botObj){
    this.modal_info_for_bot = botObj;
  }

}
