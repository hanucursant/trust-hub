import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Member } from '../../services/api.service';

@Component({
  selector: 'app-members',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 80px 20px 80px; color: white;">
      <h1>Members</h1>
      <div *ngIf="loading">Loading...</div>
      <div *ngIf="error" style="color: red;">{{ error }}</div>
      <div *ngFor="let member of members" style="margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 8px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; font-weight: 600;">
            {{ member.avatar }}
          </div>
          <div>
            <h3 style="margin: 0;">{{ member.name }}</h3>
            <p style="margin: 0; color: #999; font-size: 14px;">{{ member.role }}</p>
          </div>
        </div>
        <p style="margin-top: 10px;">Connections: {{ member.connections }}</p>
        <p *ngIf="member.isConnected" style="color: #4CAF50;">✓ Connected</p>
      </div>
    </div>
  `,
  styles: []
})
export class MembersComponent implements OnInit {
  members: Member[] = [];
  loading = false;
  error: string | null = null;
  
  constructor(private apiService: ApiService) {}
  
  ngOnInit() {
    this.loading = true;
    this.apiService.getMembers().subscribe({
      next: (data) => {
        this.members = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load members';
        this.loading = false;
        console.error('Error loading members:', err);
      }
    });
  }
}
