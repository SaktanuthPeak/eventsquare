import { isDev } from "./check-env";

export const constructCookieOptions: {
  (expires: number): {
    path: string;
    httpOnly: boolean;
    sameSite: boolean | 'lax' | 'strict' | 'none';
    secure: boolean;
    maxAge: number;
  };
} = (expires: number) => {
  return {
    // send cookie for every page
    path: '/',

    // server side only cookie so you can't use `document.cookie`
    httpOnly: true,

    // only requests from same site can send cookies
    sameSite: 'lax',


    // only sent over HTTPS in production
    secure: isDev,

    // set cookie to expire after a given time
    maxAge: expires
  };
};