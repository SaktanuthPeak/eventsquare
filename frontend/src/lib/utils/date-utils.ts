export function formatDateTime(dateString: string | Date, locale = 'th-TH', timezone?: string) {
	if (!dateString) return '';

	const date = typeof dateString === 'string' ? new Date(dateString) : dateString;
	const options: Intl.DateTimeFormatOptions = {
		day: 'numeric',
		month: 'short',
		year: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
		...(timezone ? { timeZone: timezone } : {})
	};

	return date.toLocaleDateString(locale, options);
}

export function formatDate(dateString: string | Date, locale = 'th-TH', timezone?: string) {
	if (!dateString) return '';

	try {
		const date = typeof dateString === 'string' ? new Date(dateString) : dateString;

		if (isNaN(date.getTime())) {
			return '';
		}

		const options: Intl.DateTimeFormatOptions = {
			day: 'numeric',
			month: 'short',
			year: 'numeric',
			...(timezone ? { timeZone: timezone } : {})
		};

		return date.toLocaleDateString(locale, options);
	} catch (error) {
		console.error('Error formatting date:', error);
		return '';
	}
}

export function getClientTimezone(): string {
	try {
		return Intl.DateTimeFormat().resolvedOptions().timeZone;
	} catch (error) {
		return 'th-TH';
	}
}
export function getLocalISOString(date: Date) {
	const tzoffset = date.getTimezoneOffset() * 60000; //offset in milliseconds
	const localISOString = new Date(date.getTime() - tzoffset).toISOString().slice(0, -1);
	return localISOString;
}
