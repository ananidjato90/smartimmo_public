import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-ai-assistant-panel',
  standalone: true,
  imports: [CommonModule, FormsModule, MatButtonModule, MatInputModule, MatIconModule, MatProgressSpinnerModule],
  templateUrl: './ai-assistant-panel.component.html',
  styleUrls: ['./ai-assistant-panel.component.scss']
})
export class AiAssistantPanelComponent {
  @Output() query = new EventEmitter<string>();

  prompt = '';
  isLoading = false;
  response: string | null = null;

  send(): void {
    if (!this.prompt.trim()) {
      return;
    }
    this.isLoading = true;
    this.query.emit(this.prompt.trim());
  }

  setLoading(state: boolean): void {
    this.isLoading = state;
  }

  setResponse(value: string): void {
    this.response = value;
    this.isLoading = false;
    this.prompt = '';
  }
}
