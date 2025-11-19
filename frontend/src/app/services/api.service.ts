import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Post {
  id: number;
  author: string;
  authorAvatar: string;
  authorRole: string;
  timeAgo: string;
  content: string;
  image: string;
  likes: number;
  comments: number;
  shares: number;
}

export interface Course {
  id: number;
  title: string;
  instructor: string;
  duration: string;
  level: string;
  enrolled: number;
  image: string;
}

export interface Space {
  id: number;
  name: string;
  description: string;
  members: number;
  image: string;
  isJoined: boolean;
}

export interface Member {
  id: number;
  name: string;
  role: string;
  avatar: string;
  connections: number;
  isConnected: boolean;
}

export interface Event {
  id: number;
  title: string;
  date: string;
  time: string;
  location: string;
  attendees: number;
  image: string;
  isRegistered: boolean;
}

export interface UserProfile {
  name: string;
  email: string;
  avatar: string;
  role: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:5001/api';

  constructor(private http: HttpClient) {}

  getPosts(): Observable<Post[]> {
    return this.http.get<{posts: Post[]}>(`${this.apiUrl}/posts`).pipe(
      map(response => response.posts)
    );
  }

  getCourses(): Observable<Course[]> {
    return this.http.get<{courses: Course[]}>(`${this.apiUrl}/courses`).pipe(
      map(response => response.courses)
    );
  }

  getSpaces(): Observable<Space[]> {
    return this.http.get<{spaces: Space[]}>(`${this.apiUrl}/spaces`).pipe(
      map(response => response.spaces)
    );
  }

  getMembers(): Observable<Member[]> {
    return this.http.get<{members: Member[]}>(`${this.apiUrl}/members`).pipe(
      map(response => response.members)
    );
  }

  getEvents(): Observable<Event[]> {
    return this.http.get<{events: Event[]}>(`${this.apiUrl}/events`).pipe(
      map(response => response.events)
    );
  }

  getUserProfile(): Observable<UserProfile> {
    return this.http.get<{user: UserProfile}>(`${this.apiUrl}/user/profile`).pipe(
      map(response => response.user)
    );
  }

  createPost(content: string, image?: string): Observable<Post> {
    return this.http.post<{post: Post}>(`${this.apiUrl}/posts`, { content, image }).pipe(
      map(response => response.post)
    );
  }
}
