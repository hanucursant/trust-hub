import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { JobService, Job } from '../../services/job.service';
import { AuthService, User } from '../../services/auth.service';

@Component({
  selector: 'app-feed',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './feed.component.html',
  styleUrl: './feed.component.less'
})
export class FeedComponent implements OnInit {
  selectedTab = 'All Jobs';
  tabs = ['All Jobs', 'My Jobs', 'In Progress', 'Completed'];
  jobs: Job[] = [];
  loading = false;
  error: string | null = null;
  currentUser: User | null = null;
  
  constructor(
    private jobService: JobService,
    private authService: AuthService
  ) {}
  
  ngOnInit() {
    this.authService.currentUser.subscribe(user => {
      this.currentUser = user;
    });
    this.loadData();
  }
  
  selectTab(tab: string) {
    this.selectedTab = tab;
    this.loadData();
  }
  
  loadData() {
    this.loading = true;
    this.error = null;
    
    this.jobService.getJobs().subscribe({
      next: (data) => {
        this.jobs = this.filterJobsByTab(data);
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load jobs';
        this.loading = false;
        console.error('Error loading jobs:', err);
      }
    });
  }

  filterJobsByTab(jobs: Job[]): Job[] {
    if (!this.currentUser) return [];

    switch(this.selectedTab) {
      case 'All Jobs':
        return jobs.filter(job => job.approved_by_admin);
      
      case 'My Jobs':
        if (this.currentUser.role === 'company') {
          return jobs.filter(job => job.client_id === this.currentUser!.id);
        } else if (this.currentUser.role === 'expert') {
          return jobs.filter(job => job.expert_id === this.currentUser!.id);
        }
        return [];
      
      case 'In Progress':
        return jobs.filter(job => 
          job.status === 'in_progress' && 
          (job.client_id === this.currentUser!.id || job.expert_id === this.currentUser!.id)
        );
      
      case 'Completed':
        return jobs.filter(job => 
          job.status === 'completed' && 
          (job.client_id === this.currentUser!.id || job.expert_id === this.currentUser!.id)
        );
      
      default:
        return jobs;
    }
  }

  getServiceTypeLabel(serviceType: string): string {
    return this.jobService.getServiceTypeLabel(serviceType);
  }

  getServiceTypeDescription(serviceType: string): string {
    return this.jobService.getServiceTypeDescription(serviceType);
  }

  getStatusLabel(status: string): string {
    return this.jobService.getStatusLabel(status);
  }

  getStatusClass(status: string): string {
    const statusClasses: {[key: string]: string} = {
      'draft': 'status-draft',
      'pending_approval': 'status-pending',
      'active': 'status-active',
      'in_progress': 'status-progress',
      'delivered': 'status-delivered',
      'disputed': 'status-disputed',
      'completed': 'status-completed',
      'closed': 'status-closed'
    };
    return statusClasses[status] || '';
  }

  getServiceTypeClass(serviceType: string): string {
    const serviceClasses: {[key: string]: string} = {
      'direct_trust': 'service-direct',
      'guided_trust': 'service-guided',
      'delegated_trust': 'service-delegated'
    };
    return serviceClasses[serviceType] || '';
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }
}
