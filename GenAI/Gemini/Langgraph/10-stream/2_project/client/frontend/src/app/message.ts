import { Injectable, NgZone } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { ChatEvent } from './chat-event';

@Injectable({
  providedIn: 'root',
})
export class Message {

  private eventSource?:EventSource

  constructor(private zone:NgZone){

  }


  connect(message: string, checkpointId: string | null,onEvent: (event: ChatEvent) => void){
    const encodedMessage = encodeURIComponent(message);

    let url = `http://localhost:8000/chat_stream/${encodedMessage}`;

    if (checkpointId) {
      url += `?checkpoint_id=${checkpointId}`;
    }

    this.eventSource = new EventSource(url);

    this.eventSource.onmessage = (event) => {
      this.zone.run(() => {
        try {
          const data: ChatEvent = JSON.parse(event.data);
          onEvent(data);
        } catch (err) {
          console.error('Invalid JSON from SSE:', event.data);
        }
      });
    }

    this.eventSource.onerror = (err) => {
      console.error('SSE error:', err);
      this.close();
    };
  }

  close() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = undefined;
    }
  }
}
