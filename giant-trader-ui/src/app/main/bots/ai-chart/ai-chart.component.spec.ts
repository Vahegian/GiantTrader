import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AIChartComponent } from './ai-chart.component';

describe('AIChartComponent', () => {
  let component: AIChartComponent;
  let fixture: ComponentFixture<AIChartComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AIChartComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AIChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
