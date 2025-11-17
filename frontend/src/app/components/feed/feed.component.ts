import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Post {
  id: number;
  author: {
    name: string;
    avatar: string;
    location: string;
  };
  timeAgo: string;
  content: string;
  images: string[];
}

@Component({
  selector: 'app-feed',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './feed.component.html',
  styleUrl: './feed.component.less'
})
export class FeedComponent {
  selectedTab = 'Feed';
  tabs = ['Feed', 'Spaces', 'Members', 'Courses', 'Events'];
  
  posts: Post[] = [
    {
      id: 1,
      author: {
        name: 'Todea Bianca',
        avatar: 'TB',
        location: 'Anunțuri'
      },
      timeAgo: '3d',
      content: '💥 Cu 60 de lei pe lună intri la cel mai mare eveniment VSFA+ 💥\n\nDa, ai citit bine. Cu doar 60 de lei pe lună, intri GRATUIT la FoundAIrs Summit - evenimentul în c...',
      images: ['post1-1.jpg', 'post1-2.jpg']
    }
  ];
}
