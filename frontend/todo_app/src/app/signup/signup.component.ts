import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
})
export class SignupComponent implements OnInit {
  signupObj: any = {
    username: '',
    email: '',
    password: '',
  };

  constructor(
    private http: HttpClient,
    private router: Router,
    private fb: FormBuilder
  ) {}

  signupForm!: FormGroup;
  showPasswordMismatchWarning: boolean = false;

  ngOnInit() {
    this.signupForm = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
      confirmPassword: ['', Validators.required],
    });
  }

  isFieldInvalid(field: string): boolean {
    const control = this.signupForm.get(field);
    if (control && control.invalid && (control.dirty || control.touched)) {
      return true;
    }
    return false;
  }

  onSignUp() {
    if (this.signupForm.invalid) {
      // Handle form validation errors, if any
      console.log('Form is invalid');
      return;
    }

    if (
      this.signupForm.value.password !== this.signupForm.value.confirmPassword
    ) {
      this.showPasswordMismatchWarning = true;
      console.log('Passwords do not match!');
      return;
    } else {
      this.showPasswordMismatchWarning = false;
    }

    // Access form values directly through this.signupForm.value
    const formData = {
      username: this.signupForm.value.username,
      email: this.signupForm.value.email,
      password: this.signupForm.value.password,
    };

    this.http.post('http://localhost:5000/user', formData).subscribe(
      (res: any) => {
        // Handle success response from the backend
        console.log('User registration successful:', res);
        // Optionally, you can navigate to a success page or perform other actions
        this.router.navigateByUrl('/login');
      },
      (error) => {
        // Handle error response from the backend
        console.error('Error during user registration:', error);
        // Optionally, you can display an error message to the user
      }
    );
  }
}
