export interface ChatEvent {
    type: 'checkpoint' | 'content' | 'search_start' | 'search_results' | 'end';
  checkpoint_id?: string;
  content?: string;
  query?: string;
  urls?: string[];
}
