import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Rollingday10Component } from './rollingday10.component';

describe('Rollingday10Component', () => {
  let component: Rollingday10Component;
  let fixture: ComponentFixture<Rollingday10Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Rollingday10Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Rollingday10Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
