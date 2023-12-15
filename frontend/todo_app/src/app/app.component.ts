import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  title = 'todo_app';
  isToken = localStorage.getItem('loginToken') !== null ? true : false;

  ngOnInit() {
    console.log(this.isToken);
  }
  onLogOut() {
    localStorage.removeItem('loginToken');
    this.isToken = false;
  }
}
