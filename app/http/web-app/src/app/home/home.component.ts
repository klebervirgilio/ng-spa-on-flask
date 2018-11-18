import { Component, OnInit } from '@angular/core';
import { OktaAuthService } from '@okta/okta-angular';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor(private oktaAuth: OktaAuthService) {
  }

  ngOnInit() {
  }

  async logout(event) {
    event.preventDefault();
    await this.oktaAuth.logout('/');
  }
}
