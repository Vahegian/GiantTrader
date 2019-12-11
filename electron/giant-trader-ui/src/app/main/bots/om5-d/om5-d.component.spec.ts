import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OM5DComponent } from './om5-d.component';

describe('OM5DComponent', () => {
  let component: OM5DComponent;
  let fixture: ComponentFixture<OM5DComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OM5DComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OM5DComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
