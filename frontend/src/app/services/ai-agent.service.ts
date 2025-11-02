import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';

interface AiResponse {
  response: string;
  model: string;
}

@Injectable({ providedIn: 'root' })
export class AiAgentService {
  private readonly endpoint = environment.aiEndpoint;

  constructor(private http: HttpClient) {}

  ask(prompt: string): Observable<AiResponse> {
    return this.http.post<AiResponse>(this.endpoint, { prompt });
  }
}
