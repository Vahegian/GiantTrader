import { TestBed } from '@angular/core/testing';

import { Bots } from './bots.service';

describe('Om5dDnnService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: Bots = TestBed.get(Bots);
    expect(service).toBeTruthy();
  });
});
