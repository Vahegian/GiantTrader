import { TestBed } from '@angular/core/testing';

import { EngineApiService } from './engine-api.service';

describe('EngineApiService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: EngineApiService = TestBed.get(EngineApiService);
    expect(service).toBeTruthy();
  });
});
