import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface Job {
  id: number;
  title: string;
  description: string;
  service_type: string;
  status: string;
  budget: number;
  deadline?: string;
  deliverables?: string;
  client_id: number;
  expert_id?: number;
  approved_by_admin: boolean;
  created_at: string;
  escrow?: Escrow;
  milestones?: Milestone[];
}

export interface Escrow {
  id: number;
  job_id: number;
  status: string;
  total_amount: number;
  platform_fee: number;
  funded_at?: string;
  released_at?: string;
}

export interface Milestone {
  id: number;
  job_id: number;
  title: string;
  description?: string;
  amount: number;
  deadline?: string;
  status: string;
  delivered_at?: string;
  accepted_at?: string;
}

export interface CreateJobRequest {
  title: string;
  description: string;
  service_type: 'direct_trust' | 'guided_trust' | 'delegated_trust';
  budget: number;
  deadline?: string;
  deliverables?: string;
  client_id: number;
  expert_id?: number;
}

@Injectable({
  providedIn: 'root'
})
export class JobService {
  private apiUrl = 'http://localhost:5001/api';

  constructor(private http: HttpClient) {}

  getJobs(): Observable<Job[]> {
    return this.http.get<{jobs: Job[]}>(`${this.apiUrl}/jobs`)
      .pipe(map(response => response.jobs));
  }

  getJob(id: number): Observable<Job> {
    return this.http.get<{job: Job}>(`${this.apiUrl}/jobs/${id}`)
      .pipe(map(response => response.job));
  }

  createJob(job: CreateJobRequest): Observable<Job> {
    return this.http.post<{job: Job, message: string}>(`${this.apiUrl}/jobs`, job)
      .pipe(map(response => response.job));
  }

  submitJobForApproval(jobId: number): Observable<Job> {
    return this.http.post<{job: Job, message: string}>(`${this.apiUrl}/jobs/${jobId}/submit`, {})
      .pipe(map(response => response.job));
  }

  approveJob(jobId: number): Observable<Job> {
    return this.http.post<{job: Job, message: string}>(`${this.apiUrl}/jobs/${jobId}/approve`, {})
      .pipe(map(response => response.job));
  }

  createEscrow(jobId: number): Observable<Escrow> {
    return this.http.post<{escrow: Escrow, message: string}>(`${this.apiUrl}/escrow`, { job_id: jobId })
      .pipe(map(response => response.escrow));
  }

  getServiceTypeLabel(serviceType: string): string {
    const labels: {[key: string]: string} = {
      'direct_trust': 'Direct Trust',
      'guided_trust': 'Guided Trust',
      'delegated_trust': 'Delegated Trust'
    };
    return labels[serviceType] || serviceType;
  }

  getServiceTypeDescription(serviceType: string): string {
    const descriptions: {[key: string]: string} = {
      'direct_trust': 'Self-service escrow for known expert (2% fee)',
      'guided_trust': 'Platform-assisted expert matching (7% fee)',
      'delegated_trust': 'Full project outsourcing (15% fee)'
    };
    return descriptions[serviceType] || '';
  }

  getStatusLabel(status: string): string {
    const labels: {[key: string]: string} = {
      'draft': 'Draft',
      'pending_approval': 'Pending Approval',
      'active': 'Active',
      'in_progress': 'In Progress',
      'delivered': 'Delivered',
      'disputed': 'Disputed',
      'completed': 'Completed',
      'closed': 'Closed'
    };
    return labels[status] || status;
  }
}
