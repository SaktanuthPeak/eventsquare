export interface IEvent {
  id: string;
  title: string;
  description: string;
  location: string;
  max_audience: number;
  image_id: string | null;
  start_date: string;
  end_date: string;
  created_at: string;
  image?: {
    filename: string;
    content_type: string;
    url: string;
  };
}