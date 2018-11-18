import { TestBed } from '@angular/core/testing';

import { ApiClientService } from './api-client.service';

describe('ApiClientService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ApiClientService = TestBed.get(ApiClientService);
    expect(service).toBeTruthy();
  });
});
