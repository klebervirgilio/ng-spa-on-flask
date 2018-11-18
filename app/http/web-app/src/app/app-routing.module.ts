import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';

import { OktaAuthModule, OktaCallbackComponent, OktaAuthGuard } from '@okta/okta-angular';

const routes: Routes = [
  { path: '', component: LoginComponent },
  {
    path: 'home',
    component: HomeComponent,
    canActivate: [OktaAuthGuard],
  },
  { path: 'implicit/callback', component: OktaCallbackComponent },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes),
    OktaAuthModule.initAuth({
      issuer: 'https://dev-509836.oktapreview.com/oauth2/default',
      clientId: '0oagcbm1o6GTTB9Da0h7',
      redirectUri: 'http://localhost:3000/implicit/callback',
      scope: 'openid profile email'
    })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
