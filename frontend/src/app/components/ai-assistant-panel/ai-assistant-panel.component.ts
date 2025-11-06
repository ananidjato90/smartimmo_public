import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { NgIf, NgFor } from '@angular/common';

@Component({
  selector: 'app-ai-assistant-panel',
  standalone: true,
  imports: [
    FormsModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    NgIf,
    NgFor
  ],
  templateUrl: './ai-assistant-panel.component.html',
  styleUrls: ['./ai-assistant-panel.component.scss']
})
export class AiAssistantPanelComponent {
  @Output() querySubmitted = new EventEmitter<string>();

  message = '';
  response = '';
  loading = false;

  examples = [
    'Appartement 3 chambres à Lomé',
    'Maison avec jardin à Accra',
    'Terrain constructible'
  ];

  onSubmit(): void {
    if (this.message.trim()) {
      this.querySubmitted.emit(this.message);
      this.message = '';
    }
  }

  useExample(example: string): void {
    this.message = example;
  }

  setLoading(loading: boolean): void {
    this.loading = loading;
  }

  setResponse(response: string): void {
    this.response = response;
    this.loading = false;
  }
}