export interface Integration {
  id: string;
  type: string;
  name: string;
  login: string;
  status: 'active' | 'inactive' | 'warning' | 'error';
  units: string[];
  lastSync: string;
  icon: string;
}