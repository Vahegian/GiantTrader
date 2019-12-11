import { TestBed } from '@angular/core/testing';

import { Om5dDnnService } from './om5d-dnn.service';

describe('Om5dDnnService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: Om5dDnnService = TestBed.get(Om5dDnnService);
    expect(service).toBeTruthy();
  });
});
