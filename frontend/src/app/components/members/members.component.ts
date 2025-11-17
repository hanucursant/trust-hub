import { Component } from '@angular/core';

@Component({
  selector: 'app-members',
  standalone: true,
  template: `<div class="page-container"><h2>Members</h2></div>`,
  styles: `.page-container { padding: 80px 20px 90px; } h2 { color: #fff; font-size: 24px; }`
})
export class MembersComponent {}
