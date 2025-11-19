import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Event } from '../../services/api.service';

@Component({
  selector: 'app-events',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 80px 20px 80px; color: white;">
      <h1>Events</h1>
      <div *ngIf="loading">Loading...</div>
      <div *ngIf="error" style="color: red;">{{ error }}</div>
      <div *ngFor="let event of events" style="margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 8px;">
        <h3>{{ event.title }}</h3>
        <p>📅 {{ event.date }} at {{ event.time }}</p>
        <p>📍 {{ event.location }}</p>
        <p>👥 {{ event.attendees }} attendees</p>
        <p *ngIf="event.isRegistered" style="color: #4CAF50;">✓ Registered</p>
      </div>
    </div>
  `,
  styles: []
})
export class EventsComponent implements OnInit {
  events: Event[] = [];
  loading = false;
  error: string | null = null;
  
  constructor(private apiService: ApiService) {}
  
  ngOnInit() {
    this.loading = true;
    this.apiService.getEvents().subscribe({
      next: (data) => {
        this.events = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load events';
        this.loading = false;
        console.error('Error loading events:', err);
      }
    });
  }
}
