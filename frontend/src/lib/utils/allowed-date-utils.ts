interface AllowedDates {
	date_range?: {
		start_date: string;
		end_date: string;
	};
	single_date?: string;
}

export function formatAllowedDates(allowed_dates: AllowedDates | null | undefined) {
	if (!allowed_dates) return 'No date information';

	const formatter = new Intl.DateTimeFormat('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric'
	});

	function parseDate(dateStr: string) {
		// รองรับทั้ง ISO และ Wed Feb 04 2026 14:44:24 GMT+0700 (Indochina Time)
		const date = new Date(dateStr);
		return isNaN(date.getTime()) ? null : date;
	}

	if (allowed_dates.date_range) {
		const start = parseDate(allowed_dates.date_range.start_date);
		const end = parseDate(allowed_dates.date_range.end_date);
		if (start && end) {
			return `${formatter.format(start)} - ${formatter.format(end)}`;
		}
	}

	if (allowed_dates.single_date) {
		const date = parseDate(allowed_dates.single_date);
		if (date) {
			return formatter.format(date);
		}
	}

	return 'No date information';
}