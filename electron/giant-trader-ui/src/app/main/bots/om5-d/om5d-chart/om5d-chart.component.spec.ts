import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Om5dChartComponent } from './om5d-chart.component';

describe('Om5dChartComponent', () => {
  let component: Om5dChartComponent;
  let fixture: ComponentFixture<Om5dChartComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Om5dChartComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Om5dChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
