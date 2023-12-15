import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  constructor(
    private http: HttpClient,
    private router: Router,
    private fb: FormBuilder
  ) {}

  todos: Todo[] = [];
  newTodo: string = '';
  editingIndex: number | null = null;

  ngOnInit(): void {
    // Fetch existing todos from your API
    this.http.get<Todo[]>('http://127.0.0.1:5000/tasks').subscribe(
      (res: Todo[]) => {
        console.log(res);
        if (res) {
          this.todos = res;
        }
      },
      (error) => {
        // Handle the error
        console.error('Error fetching tasks:', error);
      }
    );
    console.log(this.todos);
  }

  addTodo(): void {
    if (this.newTodo.trim() !== '') {
      const newTodo: TodoPayload = {
        task_description: this.newTodo,
        completed: false,
      };

      // Send the new todo payload to your API to store it
      this.http.post<Todo>('http://127.0.0.1:5000/tasks', newTodo).subscribe(
        (response: Todo) => {
          // Handle the response from the server
          console.log('Todo added successfully:', response);

          // Update the todos array with the response from the server
          this.todos.push(response);

          // Clear the newTodo input
          this.newTodo = '';
        },
        (error) => {
          // Handle the error from the server
          console.error('Error adding todo:', error);
        }
      );
    }
  }

  deleteTodo(id: number): void {
    this.todos = this.todos.filter((todo) => todo.user_id !== id);

    // Send a request to your API to delete the todo by ID
    // Simulate API call
    // this.todoService.deleteTodo(id).subscribe();
  }

  editTodo(index: number): void {
    this.editingIndex = index;
  }

  saveTodo(index: number): void {
    if (this.editingIndex !== null) {
      const updatedTodo: TodoUpdatePayload = {
        completed: this.todos[index].completed,
        task_description: this.todos[index].task_description,
        user_id: this.todos[index].user_id,
        task_id: this.todos[index].id,
      };
      console.log(updatedTodo);
      // Send a PUT request to update the todo by ID
      this.http.put<Todo>('http://127.0.0.1:5000/tasks', updatedTodo).subscribe(
        (response: Todo) => {
          // Handle the response from the server
          console.log('Todo updated successfully:', response);

          // Optionally, update the local todos array with the updated task
          this.todos[index] = response;

          // Reset the editingIndex
          this.editingIndex = null;
        },
        (error) => {
          // Handle the error from the server
          console.error('Error updating todo:', error);

          // Reset the editingIndex on error
          this.editingIndex = null;
        }
      );
    }
  }

  cancelEdit(): void {
    this.editingIndex = null;
  }
}

interface Todo {
  completed: boolean;
  task_description: string;
  user_id: number;
  id: number;
}

// Declare a type for the payload without the user_id
type TodoPayload = {
  task_description: string;
  completed: boolean;
};

interface TodoUpdatePayload {
  completed: boolean;
  task_description: string;
  user_id: number;
  task_id: number;
}
