import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';

interface NavItem {
  label: string;
  route: string;
  badge?: number;
}

@Component({
  selector: 'app-bottom-nav',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './bottom-nav.component.html',
  styleUrl: './bottom-nav.component.less'
})
export class BottomNavComponent {
  navItems: NavItem[] = [
    { label: 'Feed', route: '/feed', badge: 2 },
    { label: 'Spaces', route: '/spaces' },
    { label: 'Members', route: '/members' },
    { label: 'Courses', route: '/courses' },
    { label: 'Events', route: '/events', badge: 1 }
  ];
}
