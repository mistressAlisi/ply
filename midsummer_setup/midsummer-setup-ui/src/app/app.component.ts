import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {NgForOf, NgIf} from "@angular/common";
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NgForOf, NgIf, ReactiveFormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'midsummer-setup-ui';
  steps = [
    { header: 'Database Credentials', subtext: 'Connect to your Database' },
    { header: 'Community Details', subtext: 'General information about your community' },
    { header: 'Module Selections', subtext: 'Select the modules you want to use in your application.'},
    { header: 'Module Setups', subtext: 'Setup selected modules'},
    { header: 'Mail Credentials', subtext: 'Setup your mail credentials' },
    { header: 'Static File Storage', subtext: 'Choose where Static and Media files will be stored' },
    { header: 'Stripe Payments', subtext: 'Connect to your Stripe account' },
  ]
  step: number = 1;

  dbForm = new FormGroup({
    db_host: new FormControl(''),
    db_port: new FormControl(''),
    db_user: new FormControl(''),
    db_pass: new FormControl(''),
    db_name: new FormControl(''),
  });

}
