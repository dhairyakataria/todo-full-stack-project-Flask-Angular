import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  loginError!: string;
  invalidCredentialsError!: string;

  constructor(
    private http: HttpClient,
    private router: Router,
    private fb: FormBuilder
  ) {}

  ngOnInit() {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
  }

  isFieldInvalid(field: string): boolean {
    const control = this.loginForm.get(field);
    return (
      control !== null && control.invalid && (control.dirty || control.touched)
    );
  }
  onLogin() {
    if (this.loginForm.invalid) {
      // The form is not valid, handle accordingly
      console.log('Form is invalid');
      return;
    }

    console.log(this.loginForm.value);

    this.http
      .post('http://127.0.0.1:5000/login', this.loginForm.value)
      .subscribe(
        (res: any) => {
          if (res.log_in) {
            localStorage.setItem('loginToken', res.access_token);
            this.router.navigateByUrl('/home');
          } else {
            alert(res.message);
          }
        },

        (error) => {
          if (error.status === 401) {
            // Check if the error response indicates invalid username/password
            if (
              error.error &&
              error.error.message &&
              error.error.message
                .toLowerCase()
                .includes('invalid username or password')
            ) {
              this.invalidCredentialsError = 'Invalid username or password';
              this.loginError = ''; // Clear other errors
            } else {
              // Handle other 401 errors
              this.invalidCredentialsError = '';
              this.loginError = 'Invalid credentials';
            }
          } else {
            // Handle other errors
            this.invalidCredentialsError = '';
            this.loginError = 'An error occurred. Please try again.';
            console.error('An error occurred:', error);
          }
        }
      );
  }
}
