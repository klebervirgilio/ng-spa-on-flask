import { TestBed } from '@angular/core/testing';

import { GithubClientService } from './github-client.service';

describe('GithubClientService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: GithubClientService = TestBed.get(GithubClientService);
    expect(service).toBeTruthy();
  });
});
