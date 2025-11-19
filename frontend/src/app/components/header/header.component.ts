import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.less'
})
export class HeaderComponent implements OnInit, OnDestroy {
  userInitials = 'CV';
  userName = '';
  showUserMenu = false;
  isLoggedIn = false;
  private userSubscription?: Subscription;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    // Subscribe to user changes to reactively update the UI
    this.userSubscription = this.authService.currentUser.subscribe(user => {
      if (user) {
        this.isLoggedIn = true;
        this.userName = user.name;
        const nameParts = user.name.split(' ');
        this.userInitials = nameParts.length > 1 
          ? nameParts[0][0] + nameParts[1][0]
          : nameParts[0][0] + (nameParts[0][1] || '');
        this.userInitials = this.userInitials.toUpperCase();
      } else {
        this.isLoggedIn = false;
        this.userName = '';
        this.userInitials = '';
      }
    });
  }

  ngOnDestroy() {
    // Clean up subscription to prevent memory leaks
    if (this.userSubscription) {
      this.userSubscription.unsubscribe();
    }
  }

  toggleUserMenu() {
    this.showUserMenu = !this.showUserMenu;
  }

  logout() {
    this.showUserMenu = false;
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
