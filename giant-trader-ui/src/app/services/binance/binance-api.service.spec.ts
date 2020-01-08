import { TestBed } from '@angular/core/testing';

import { BinanceApiService } from './binance-api.service';

describe('EngineApiService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: BinanceApiService = TestBed.get(BinanceApiService);
    expect(service).toBeTruthy();
  });
});
