import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Course } from '../../services/api.service';

@Component({
  selector: 'app-courses',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 80px 20px 80px; color: white;">
      <h1>Courses</h1>
      <div *ngIf="loading">Loading...</div>
      <div *ngIf="error" style="color: red;">{{ error }}</div>
      <div *ngFor="let course of courses" style="margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 8px;">
        <h3>{{ course.title }}</h3>
        <p>Instructor: {{ course.instructor }}</p>
        <p>Duration: {{ course.duration }} | Level: {{ course.level }}</p>
        <p>Enrolled: {{ course.enrolled }} students</p>
      </div>
    </div>
  `,
  styles: []
})
export class CoursesComponent implements OnInit {
  courses: Course[] = [];
  loading = false;
  error: string | null = null;
  
  constructor(private apiService: ApiService) {}
  
  ngOnInit() {
    this.loading = true;
    this.apiService.getCourses().subscribe({
      next: (data) => {
        this.courses = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load courses';
        this.loading = false;
        console.error('Error loading courses:', err);
      }
    });
  }
}
