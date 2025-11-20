import { Routes } from '@angular/router';
import { FeedComponent } from './components/feed/feed.component';
import { SpacesComponent } from './components/spaces/spaces.component';
import { MembersComponent } from './components/members/members.component';
import { CoursesComponent } from './components/courses/courses.component';
import { EventsComponent } from './components/events/events.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { CreateJobComponent } from './components/create-job/create-job.component';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: '', redirectTo: '/feed', pathMatch: 'full' },
  { path: 'feed', component: FeedComponent, canActivate: [AuthGuard] },
  { path: 'create-job', component: CreateJobComponent, canActivate: [AuthGuard] },
  { path: 'spaces', component: SpacesComponent, canActivate: [AuthGuard] },
  { path: 'members', component: MembersComponent, canActivate: [AuthGuard] },
  { path: 'courses', component: CoursesComponent, canActivate: [AuthGuard] },
  { path: 'events', component: EventsComponent, canActivate: [AuthGuard] }
];
