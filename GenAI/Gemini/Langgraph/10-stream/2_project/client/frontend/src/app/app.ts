import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Message } from './message';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
  userInput=''
  isTyping=signal(false)
  messages = signal<{role: 'user' | 'assistant', text: string, searchQuery?: string, searchUrls?: string[]}[]>([{ role: 'assistant', text: "Hello! I've finished analyzing the repository. What would you like to know about the codebase?", searchQuery: '', searchUrls: []}]);
  checkpointId: string | null = null;
  isSearching = false;
  searchUrls:string[]=[]
  searchQuery = '';

  constructor(private message: Message){

  }

  send(){
    const question=this.userInput
    this.userInput='';
    this.isTyping.set(true);
    this.messages.set([...this.messages(),{role:'user',text:question, searchQuery: '', searchUrls: []}])
    this.messages.set([...this.messages(),{role:'assistant',text:'', searchQuery: '', searchUrls: []}])
    this.message.connect(question,this.checkpointId,(event)=>{
      switch(event.type){
        case 'checkpoint':
          this.checkpointId=event.checkpoint_id!
          break;
        
        case 'content':
          this.messages.update(msgs => {
            const updated = [...msgs];
            const lastIndex = updated.length - 1;
          
            updated[lastIndex] = {
              ...updated[lastIndex],
              text: updated[lastIndex].text + event.content
            };
            
            return updated;
          });
          
          break;
        
        case 'search_start':
          this.isSearching=true;
          this.searchQuery=event.query!;
          // this.messages.set([...this.messages(),{role:'assistant',text:this.currentBotMessage, searchQuery: this.searchQuery, searchUrls: this.searchUrls}])
          this.messages.update(msgs => {
            const updated = [...msgs];
            const lastIndex = updated.length - 1;
          
            updated[lastIndex] = {
              ...updated[lastIndex],
              searchQuery: event.query
            };
            return updated;
          });
          console.log('Search started for query:', event.query);
          break;
        
        case 'search_results':
          this.isSearching=false;
          // this.searchUrls=event.urls || [];
          this.searchUrls=event.urls || [];
          // this.messages.set([...this.messages(),{role:'assistant',text:this.currentBotMessage, searchQuery: this.searchQuery, searchUrls: this.searchUrls}])
          this.messages.update(msgs => {
            const updated = [...msgs];
            const lastIndex = updated.length - 1;
          
            updated[lastIndex] = {
              ...updated[lastIndex],
              searchUrls: event.urls
            };
            return updated;
          });
          console.log('Search results:', this.searchUrls);
          break;

        case 'end':
          this.isTyping.set(false);
          // this.message.messagesSub.next([...this.messages(),{role:'assistant',text:this.currentBotMessage, searchQuery: this.searchQuery, searchUrls: this.searchUrls}])
          this.isSearching=false;
          this.searchUrls=[];
          this.message.close();
          break;
      }
    })
  }
}
