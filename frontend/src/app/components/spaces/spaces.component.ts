import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Space } from '../../services/api.service';

@Component({
  selector: 'app-spaces',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 80px 20px 80px; color: white;">
      <h1>Spaces</h1>
      <div *ngIf="loading">Loading...</div>
      <div *ngIf="error" style="color: red;">{{ error }}</div>
      <div *ngFor="let space of spaces" style="margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 8px;">
        <h3>{{ space.name }}</h3>
        <p>{{ space.description }}</p>
        <p>Members: {{ space.members }}</p>
        <p *ngIf="space.isJoined" style="color: #4CAF50;">✓ Joined</p>
      </div>
    </div>
  `,
  styles: []
})
export class SpacesComponent implements OnInit {
  spaces: Space[] = [];
  loading = false;
  error: string | null = null;
  
  constructor(private apiService: ApiService) {}
  
  ngOnInit() {
    this.loading = true;
    this.apiService.getSpaces().subscribe({
      next: (data) => {
        this.spaces = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load spaces';
        this.loading = false;
        console.error('Error loading spaces:', err);
      }
    });
  }
}
