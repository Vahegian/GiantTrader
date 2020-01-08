import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {FormsModule} from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { BinanceApiService } from './services/binance/binance-api.service';
import { HttpClientModule } from '@angular/common/http';
import { MainComponent } from './main/main/main.component';
import { TopComponent } from './main/top/top.component';
import { ExchangeComponent } from './main/exchange/exchange.component';
import { WalletComponent } from './main/exchange/wallet/wallet.component';
import { OpenOrdersComponent } from './main/exchange/open-orders/open-orders.component';
import { LimitOrdersComponent } from './main/exchange/limit-orders/limit-orders.component';
import { BotsComponent } from './main/bots/bots.component';
import { ChartComponent } from './main/exchange/chart/chart.component';
import { ChartsModule } from 'ng2-charts';
import { AIChartComponent } from './main/bots/ai-chart/ai-chart.component';
import { AI } from './services/ai/ai.service';
import { Bots } from './services/bots/bots.service';
import { ChartLiveComponent } from './main/exchange/chart-live/chart-live.component';
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    MainComponent,
    TopComponent,
    ExchangeComponent,
    WalletComponent,
    OpenOrdersComponent,
    LimitOrdersComponent,
    BotsComponent,
    ChartComponent,
    AIChartComponent,
    ChartLiveComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ChartsModule
  ],
  providers: [BinanceApiService, AI, Bots],
  bootstrap: [AppComponent]
})
export class AppModule { }
