export type UserRole = ['admin' | 'user'];

export interface IUser {
  id?: string;
  email: string;
  username: string;
  password: string;
  confirm_password?: string;
  first_name?: string;
  last_name?: string;
  status?: string;
  roles?: UserRole[];
}