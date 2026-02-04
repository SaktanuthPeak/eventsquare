import pino from 'pino';
import { env } from '$env/dynamic/private';

let transport: pino.LoggerOptions['transport'];

if (env.NODE_ENV === 'development') {
	transport = {
		target: 'pino-pretty',
		options: {
			colorize: true,
			translateTime: 'yyyy-mm-dd HH:MM:ss.l'
		}
	};
}

export const logger = pino({
	level: env.NODE_ENV === 'development' ? 'debug' : 'info',
	formatters: {
		log(object) {
			if (object instanceof Request) {
				const url = new URL(object.url);
				return {
					method: object.method,
					url: object.url,
					path: url.pathname,
					query: url.searchParams.toString(),
					agent: object.headers.get('user-agent')
				};
			}
			return object;
		},
	},
	transport
});

export const requestInfo = (request: Request, status?: number) => {
	const url = new URL(request.url);
	return `${request.method}: ${url.pathname}` + (status ? ` - ${status}` : '');
};