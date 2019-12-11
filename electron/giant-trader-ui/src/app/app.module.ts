import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {FormsModule} from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { EngineApiService } from './services/engine/engine-api.service';
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
import { OM5DComponent } from './main/bots/om5-d/om5-d.component';
import { Om5dChartComponent } from './main/bots/om5-d/om5d-chart/om5d-chart.component';
import { Om5dDnnService } from './services/om5d/om5d-dnn.service';

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
    OM5DComponent,
    Om5dChartComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ChartsModule
  ],
  providers: [EngineApiService, Om5dDnnService],
  bootstrap: [AppComponent]
})
export class AppModule { }
