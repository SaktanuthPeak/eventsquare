export const constructCookieOptions: {
  (expires: number, secureOrUrl?: boolean | URL): {
    path: string;
    httpOnly: boolean;
    sameSite: boolean | 'lax' | 'strict' | 'none';
    secure: boolean;
    maxAge: number;
  };
} = (expires: number, secureOrUrl?: boolean | URL) => {
  const secure =
    typeof secureOrUrl === 'boolean'
      ? secureOrUrl
      : secureOrUrl instanceof URL
        ? secureOrUrl.protocol === 'https:'
        : false;

  return {
    path: '/',
    httpOnly: true,
    sameSite: 'lax',
    secure,
    maxAge: expires
  };
};