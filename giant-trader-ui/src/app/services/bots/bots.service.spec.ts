import { TestBed } from '@angular/core/testing';

import { RollingDayBot } from './bots.service';

describe('Om5dDnnService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: RollingDayBot = TestBed.get(RollingDayBot);
    expect(service).toBeTruthy();
  });
});
