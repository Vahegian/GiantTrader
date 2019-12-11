import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LimitOrdersComponent } from './limit-orders.component';

describe('LimitOrdersComponent', () => {
  let component: LimitOrdersComponent;
  let fixture: ComponentFixture<LimitOrdersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LimitOrdersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LimitOrdersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
