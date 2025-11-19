import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService, Post, Space, Member, Course, Event } from '../../services/api.service';

@Component({
  selector: 'app-feed',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './feed.component.html',
  styleUrl: './feed.component.less'
})
export class FeedComponent implements OnInit {
  selectedTab = 'Feed';
  tabs = ['Feed', 'Spaces', 'Members', 'Courses', 'Events'];
  posts: Post[] = [];
  spaces: Space[] = [];
  members: Member[] = [];
  courses: Course[] = [];
  events: Event[] = [];
  loading = false;
  error: string | null = null;
  
  constructor(private apiService: ApiService) {}
  
  ngOnInit() {
    this.loadData();
  }
  
  selectTab(tab: string) {
    this.selectedTab = tab;
    this.loadData();
  }
  
  loadData() {
    this.loading = true;
    this.error = null;
    
    switch(this.selectedTab) {
      case 'Feed':
        this.loadPosts();
        break;
      case 'Spaces':
        this.loadSpaces();
        break;
      case 'Members':
        this.loadMembers();
        break;
      case 'Courses':
        this.loadCourses();
        break;
      case 'Events':
        this.loadEvents();
        break;
    }
  }
  
  loadPosts() {
    this.apiService.getPosts().subscribe({
      next: (data) => {
        this.posts = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load posts';
        this.loading = false;
        console.error('Error loading posts:', err);
      }
    });
  }
  
  loadSpaces() {
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
  
  loadMembers() {
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
  
  loadCourses() {
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
  
  loadEvents() {
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
