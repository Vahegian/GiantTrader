import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartLiveComponent } from './chart-live.component';

describe('ChartLiveComponent', () => {
  let component: ChartLiveComponent;
  let fixture: ComponentFixture<ChartLiveComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChartLiveComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChartLiveComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
