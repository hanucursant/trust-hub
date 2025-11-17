import { Routes } from '@angular/router';
import { FeedComponent } from './components/feed/feed.component';
import { SpacesComponent } from './components/spaces/spaces.component';
import { MembersComponent } from './components/members/members.component';
import { CoursesComponent } from './components/courses/courses.component';
import { EventsComponent } from './components/events/events.component';

export const routes: Routes = [
  { path: '', redirectTo: '/feed', pathMatch: 'full' },
  { path: 'feed', component: FeedComponent },
  { path: 'spaces', component: SpacesComponent },
  { path: 'members', component: MembersComponent },
  { path: 'courses', component: CoursesComponent },
  { path: 'events', component: EventsComponent }
];
