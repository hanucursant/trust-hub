import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { JobService, CreateJobRequest } from '../../services/job.service';
import { AuthService, User } from '../../services/auth.service';

@Component({
  selector: 'app-create-job',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './create-job.component.html',
  styleUrl: './create-job.component.less'
})
export class CreateJobComponent implements OnInit {
  currentUser: User | null = null;
  
  // Form fields
  title = '';
  description = '';
  serviceType: 'direct_trust' | 'guided_trust' | 'delegated_trust' = 'guided_trust';
  budget = 0;
  deadline = '';
  deliverables = '';
  expertId?: number;
  
  // UI state
  loading = false;
  error: string | null = null;
  success = false;
  
  serviceTypes = [
    {
      value: 'direct_trust',
      label: 'Direct Trust (2% fee)',
      description: 'You have identified an expert and want secure escrow for payment',
      fee: 2
    },
    {
      value: 'guided_trust',
      label: 'Guided Trust (7% fee)',
      description: 'Platform helps match you with verified experts',
      fee: 7
    },
    {
      value: 'delegated_trust',
      label: 'Delegated Trust (15% fee)',
      description: 'Full project management by the platform',
      fee: 15
    }
  ];

  constructor(
    private jobService: JobService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.authService.currentUser.subscribe(user => {
      this.currentUser = user;
      
      // Redirect if not a company
      if (user && user.role !== 'company') {
        this.router.navigate(['/']);
      }
    });
  }

  getSelectedServiceType() {
    return this.serviceTypes.find(st => st.value === this.serviceType);
  }

  selectServiceType(value: string) {
    this.serviceType = value as 'direct_trust' | 'guided_trust' | 'delegated_trust';
  }

  calculatePlatformFee(): number {
    if (!this.budget) return 0;
    const serviceType = this.getSelectedServiceType();
    return serviceType ? (this.budget * serviceType.fee / 100) : 0;
  }

  calculateTotalCost(): number {
    return this.budget + this.calculatePlatformFee();
  }

  onSubmit() {
    // Validation
    if (!this.title.trim()) {
      this.error = 'Job title is required';
      return;
    }

    if (!this.description.trim()) {
      this.error = 'Job description is required';
      return;
    }

    if (this.budget <= 0) {
      this.error = 'Budget must be greater than 0';
      return;
    }

    if (!this.currentUser) {
      this.error = 'You must be logged in to create a job';
      return;
    }

    this.error = null;
    this.loading = true;

    const jobData: CreateJobRequest = {
      title: this.title,
      description: this.description,
      service_type: this.serviceType,
      budget: this.budget,
      client_id: this.currentUser.id
    };

    // Add optional fields
    if (this.deadline) {
      jobData.deadline = this.deadline;
    }

    if (this.deliverables.trim()) {
      jobData.deliverables = this.deliverables;
    }

    if (this.expertId) {
      jobData.expert_id = this.expertId;
    }

    this.jobService.createJob(jobData).subscribe({
      next: (job) => {
        this.success = true;
        this.loading = false;
        
        // Reset form
        setTimeout(() => {
          this.router.navigate(['/']);
        }, 2000);
      },
      error: (err) => {
        this.error = err.error?.message || 'Failed to create job';
        this.loading = false;
        console.error('Error creating job:', err);
      }
    });
  }

  cancel() {
    this.router.navigate(['/']);
  }
}
